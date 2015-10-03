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
from collections import defaultdict

from animanager import inputlib
from animanager import trashlib

from .bump import bump

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=main)


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
        self._files = defaultdict(list)

    def match(self, filename):
        """Attempt to add a file.

        Return True if successful, else False.

        """
        match = self._pattern.match(filename)
        if match:
            # Even if we match a file, we still check the episode number.
            # If it has already been watched, remove the file and don't add
            # it.
            episode = int(match.group('ep'))
            self._files[episode].append(filename)
            return True
        else:
            return False

    def has_next(self):
        """Return whether there are files for the next episode."""
        return self.next_ep in self._files

    def peek(self):
        """Return the list of files for the next episode."""
        return self._files[self.next_ep]

    @property
    def next_ep(self):
        """Return the integer of the next episode."""
        return self.ep_watched + 1

    def pop(self):
        """Pop an episode.

        Trash the files for the next episode and remove it from our structures.

        """
        for file in self._files[self.next_ep]:
            trashlib.trash(file)
        del self._files[self.next_ep]
        self.ep_watched = self.next_ep

    def __bool__(self):
        return bool(self._files)

    def __len__(self):
        return len(self._files)

    def clean(self):
        """Trash unneeded files."""
        for ep in [ep for ep in self._files.keys() if ep <= self.ep_watched]:
            for file in self._files[ep]:
                trashlib.trash(file)
            del self._files[ep]


def _load_series_info(db, config):
    """Load series info.

    Read series id and filename patterns from the config file and match it with
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


def _load_files(series_list, files):
    """Match series files.

    Use series information to associate with the given list of files.

    """
    for filename in files:
        for info in series_list:
            if info.match(filename):
                break
    return [info for info in series_list if info]


def _file_ext(filename):
    """Return file extension."""
    return os.path.splitext(filename)[1]

_VIDEO_EXT = set(('.mkv', '.mp4'))


def main(args):

    config = args.config
    db = args.db
    player_args = shlex.split(config['watch']['player'])

    # Load series information.
    series_list = _load_series_info(db, config)

    # Use series information to search current directory for files and
    # match them with a series.
    files = [file
             for file in sorted(os.listdir('.'))
             if _file_ext(file) in _VIDEO_EXT]
    series_list = _load_files(series_list, files)
    del files

    # Clean up unneeded files.
    for x in series_list:
        x.clean()
    # Remove series that no longer have any files.
    series_list = [x for x in series_list if x]

    while series_list:
        # Choose series to watch.
        msg = "({id}) {name} (cur. {cur}, avail. {avail}){missing}"
        i = inputlib.get_choice(
            [msg.format(id=info.id, name=info.name, cur=info.ep_watched,
                        avail=len(info),
                        missing='' if info.has_next() else ' (missing)')
             for info in series_list]
        )

        info = series_list[i]

        # Check if we have the next episode.
        if not info.has_next():
            print('Next episode is missing.')
            continue

        # Choose the file to play if there is more than one.
        files = info.peek()
        if len(files) > 1:
            i = inputlib.get_choice(files)
            file = files[i]
            del files
        else:
            file = files[0]
        # Play the episode.
        subprocess.call(player_args + [file])
        del file

        if inputlib.get_yn('Bump?'):
            bump(db, info.id)
            # Remove the episode from our list.
            info.pop()

        # Filter out series that have no files.
        series_list = [x for x in series_list if x]
