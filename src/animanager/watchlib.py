# Copyright (C) 2015-2016  Allen Li
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
This module contains stuff needed to set up the watching of anime.
"""

import logging
import os
import re
from collections import defaultdict

from animanager import trashlib

_LOGGER = logging.getLogger(__name__)
_VIDEO_EXT = set(('.mkv', '.mp4'))


def _file_ext(filename):
    """Return file extension."""
    return os.path.splitext(filename)[1]


class SeriesInfo:

    """Used for processing the files for a given series.

    First add all files using match().  Afterward, call prep(), then use next()
    and pop() to process the remaining files in sequence.

    """

    def __init__(self, id, pattern, name, ep_watched):
        self.id = id
        self._pattern = re.compile(pattern, re.I)
        self.name = name
        self.ep_watched = ep_watched
        self._files = defaultdict(list)

    def add(self, filename):
        """Attempt to add a file.

        Return True if successful, else False.

        """
        match = self._pattern.search(os.path.basename(filename))
        if match:
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

        Return the files for the next episode and remove it from our
        structures.

        """
        old = self._files[self.next_ep]
        del self._files[self.next_ep]
        self.ep_watched = self.next_ep
        return old

    def __bool__(self):
        return bool(self._files)

    def __len__(self):
        return len(self._files)

    def clean(self):
        """Return list of unneeded files."""
        unneeded = []
        for ep in [ep for ep in self._files.keys() if ep <= self.ep_watched]:
            for file in self._files[ep]:
                unneeded.append(file)
            del self._files[ep]
        return unneeded


def load_series_info(db, config):
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
        processed_list.append(SeriesInfo(id, pattern, name, ep_watched))
    return processed_list


def find_files(config):
    """Find video files to watch."""
    dir = config['watch'].getpath('directory')
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if os.stat(dirpath) == os.stat(trashlib.trashdir(config)):
                continue
            file = os.path.join(dirpath, filename)
            if _file_ext(file) in _VIDEO_EXT:
                files.append(file)
    return sorted(files)


def load_files(series_list, files):
    """Match series files.

    Use series information to associate with the given list of files.

    """
    for filename in files:
        for info in series_list:
            if info.add(filename):
                break
    return [info for info in series_list if info]
