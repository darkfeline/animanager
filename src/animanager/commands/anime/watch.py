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
import re
from operator import itemgetter
from collections import namedtuple
from collections import deque

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

_EpisodeInfo = namedtuple("_EpisodeInfo", ['ep_num', 'file'])


class _SeriesInfo:

    def __init__(self, id, pattern, name, ep_watched):
        self.id = id
        self.pattern = re.compile(pattern)
        self.name = name
        self.ep_watched = ep_watched
        self.matched_files = list()

    def add(self, ep_num, file):
        self.matched_files.append(_EpisodeInfo(ep_num, file))

    @property
    def next(self):
        return self.matched_files[0]

    def pop(self):
        return self.matched_files.popleft()

    def sort(self):
        self.matched_files = deque(
            sorted(self.matched_files, key=itemgetter(0)))

    def __bool__(self):
        return bool(self.matched_files)

    def __len__(self):
        return len(self.matched_files)


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


def _match_series_files(series_info, files):
    """Match series files.

    Use series information to associate with the given list of files.

    """
    for filename in files:
        for info in series_info:
            match = info.pattern.match(filename)
            if match:
                # Even if we match a file, we still check the episode number.
                # If it has already been watched, remove the file and don't add
                # it.
                ep_num = int(match.group('ep'))
                if ep_num <= info.ep_watched:
                    os.remove(filename)
                    msg = 'Removed {} because it has already been watched.'
                    _LOGGER.info(msg.format(filename))
                else:
                    info.add(ep_num, filename)
                break
    for info in series_info:
        info.sort()
    return [info for info in series_info if info]

_VIDEO_EXT = set(('.mkv', '.mp4'))


def main(args):

    config = args.config
    db = args.db
    player = config['watch']['player']

    # Load series information.
    series_info = _get_series_info(db, config)

    # Use series information to search current directory for files and
    # match them with a series.
    files = [file
             for file in sorted(os.listdir('.'))
             if os.path.splitext(file)[1] in _VIDEO_EXT]
    series_info = _match_series_files(series_info, files)
    del files

    while series_info:
        # Choose series to watch.
        msg = "({}) {} (cur. ep. {}, {} eps. avail.)"
        i = inputlib.get_choice(
            [msg.format(info.id, info.name, info.ep_watched, len(info))
             for info in series_info]
        )

        info = series_info[i]

        # Check if next episode has the right number.
        if info.next.ep_num != info.ep_watched + 1:
            print('Next episode is missing.')
            continue

        # Play the episode.
        subprocess.call([player, info.next.file])

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
