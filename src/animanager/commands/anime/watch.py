# Copyright (C) 2015  Allen Li
#
# This file is part of Animanager.
#
# Animanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Animanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Animanager.  If not, see <http://www.gnu.org/licenses/>.

"""
Automated anime watching and tracking script.
"""

import logging
import os
import subprocess
import shlex
import re
from collections import namedtuple
from collections import deque
import itertools

from animanager import inputlib

from .bump import bump

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=main)

_EpisodeInfo = namedtuple("_EpisodeInfo", ['episode', 'version', 'file'])


class _SeriesInfo:

    """Used for processing the files for a given series.

    First add all files using match().  Afterward, call prep(), then use next()
    and pop() to process the remaining files in sequence.

    """

    def __init__(self, id, pattern, name, ep_watched):
        self.id = id
        self._pattern = re.compile(pattern)
        self.name = name
        self.ep_watched = ep_watched
        self._matched_files = list()

    def match(self, filename):
        """Attempt to add a file.

        Return the _EpisodeInfo if successful, else None.

        """
        match = self._pattern.match(filename)
        if match:
            # Even if we match a file, we still check the episode number.
            # If it has already been watched, remove the file and don't add
            # it.
            episode = int(match.group('ep'))
            version = match.group('ver')
            version = int(version) if version is not None else 1
            info = _EpisodeInfo(episode, version, filename)
            self._matched_files.append(info)
            return info
        else:
            return None

    @property
    def next(self):
        return self._matched_files[0]

    def pop(self):
        return self._matched_files.popleft()

    def prep(self):
        """Prep for use after adding files."""
        self._sort()

    @property
    def missing(self):
        """Return whether the next episode to watch is missing."""
        return self.next.episode != self.ep_watched + 1

    def _sort(self):
        """Sort matched files and put into deque for processing."""
        # First sort by version reversed, then by episode.
        # Final looks like: 1v2, 1v1, 2v2, 2v1
        x = self._matched_files
        x = sorted(x, key=lambda x: x.version, reverse=True)
        x = sorted(x, key=lambda x: x.episode)
        self._matched_files = deque(x)

    def __bool__(self):
        return bool(self._matched_files)

    def __len__(self):
        return len(self._matched_files)

    def unneeded(self):
        """Return list of unneeded episodes."""
        # The goal is to find all the files we don't need.  Specifically,
        # these are files of episodes that have already been watched or files
        # that have a newer version already.
        #
        # This assumes the file list has already been sorted.
        #
        # We use an index that says, all files with an episode less than this
        # is unneeded.
        unneeded = []
        cur_ep = self.ep_watched
        i = 0
        while i < len(self._matched_files):
            episode_info = self._matched_files[i]
            if episode_info.episode <= cur_ep:
                unneeded.append(episode_info.file)
                del self._matched_files[i]
            else:
                cur_ep = episode_info.episode
                i += 1
        return unneeded


def _get_series_info(db, config):
    """Get series info.

    Load series id and filename patterns from the config file and match it with
    other necessary info from our database.

    """
    processed_list = []
    for id, pattern in config['series'].items():
        id = int(id)
        # Get series information from database.
        results = db.select(
            table='anime',
            fields=['name', 'ep_watched'],
            where_filter='id=?',
            where_args=(id,),
        )
        name, ep_watched = list(results)[0]
        processed_list.append(_SeriesInfo(id, pattern, name, ep_watched))
    return processed_list


def _series_load_files(series_info, files):
    """Match series files.

    Use series information to associate with the given list of files.

    """
    for filename in files:
        for info in series_info:
            if info.match(filename):
                break
    for info in series_info:
        info.prep()
    return [info for info in series_info if info]

_VIDEO_EXT = set(('.mkv', '.mp4'))


def main(args):

    config = args.config
    db = args.db
    player_args = shlex.split(config['watch']['player'])

    # Load series information.
    series_info = _get_series_info(db, config)

    # Use series information to search current directory for files and
    # match them with a series.
    files = [file
             for file in sorted(os.listdir('.'))
             if os.path.splitext(file)[1] in _VIDEO_EXT]
    series_info = _series_load_files(series_info, files)
    del files

    # Clean up unneeded files
    unneeded = list(itertools.chain(*(x.unneeded() for x in series_info)))
    if unneeded:
        print('Found unneeded:')
        for x in unneeded:
            print(x)
        if inputlib.get_yn('Delete?'):
            for x in unneeded:
                os.remove(x)
    # Remove series that now have no files
    series_info = [x for x in series_info if x]

    while series_info:
        # Choose series to watch.
        msg = "({id}) {name} (cur. {cur}, avail. {avail}){missing}"
        i = inputlib.get_choice(
            [msg.format(id=info.id, name=info.name, cur=info.ep_watched,
                        avail=len(info),
                        missing=' (missing)' if info.missing else '')
             for info in series_info]
        )

        info = series_info[i]

        # Check if next episode has the right number.
        if info.missing:
            print('Next episode is missing.')
            continue

        # Play the episode.
        subprocess.call(player_args + [info.next.file])

        if inputlib.get_yn('Bump?'):
            bump(db, info.id)
            info.ep_watched += 1

        if inputlib.get_yn('Delete?'):
            os.unlink(info.next.file)
            # Remove the episode from our list.
            info.pop()
            # Also remove the series if there are no more episodes.
            if not info:
                del series_info[i]
