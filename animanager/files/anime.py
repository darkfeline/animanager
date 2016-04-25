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

"""Anime file tools."""

import json
import os
import re
from collections import defaultdict
from itertools import chain
from typing import Iterable, Set


class AnimeFiles:

    r"""Used for matching and grouping files for an anime.

    >>> x = AnimeFiles(r'madoka.*?(?P<ep>\d+)')
    >>> x.add('madoka - 01.mkv')
    >>> x.add('madoka - 01v2.mkv')
    >>> x.add('madoka - 02.mkv')
    >>> x.add('utawarerumono - 01.mkv')
    >>> list(x)
    [1, 2]
    >>> x.available_string(0)
    '1,2'
    >>> x[1] == {'madoka - 01.mkv', 'madoka - 01v2.mkv'}
    True

    """

    EPISODES_TO_SHOW = 6

    def __init__(self, regexp: str, filenames: Iterable = ()) -> None:
        self.regexp = re.compile(regexp, re.I)
        # Maps episode int to list of filename strings.
        self.by_episode = defaultdict(set)
        self.add_iter(filenames)

    def __getitem__(self, episode: int) -> Set[str]:
        return self.by_episode[episode]

    def __contains__(self, episode: int) -> bool:
        return episode in self.by_episode

    def __iter__(self):
        return iter(sorted(self.by_episode))

    def __repr__(self):
        return 'AnimeFiles({}, {})'.format(
            self.regexp.pattern,
            self.filenames,
        )

    def add(self, filename):
        """Try to add a file."""
        basename = os.path.basename(filename)
        match = self.regexp.search(basename)
        if match:
            self.by_episode[int(match.group('ep'))].add(filename)

    def add_iter(self, filenames):
        """Try to add files."""
        for filename in filenames:
            self.add(filename)

    def available_string(self, episode):
        """Return a string of available episodes."""
        available = [ep for ep in self if ep > episode]
        string = ','.join(str(ep) for ep in available[:self.EPISODES_TO_SHOW])
        if len(available) > self.EPISODES_TO_SHOW:
            string += '...'
        return string

    @property
    def filenames(self):
        """Added filenames."""
        return list(chain(*self.by_episode.values()))

    def to_json(self):
        """Export AnimeFiles to JSON string."""
        return json.dumps({
            'regexp': self.regexp.pattern,
            'files': self.filenames,
        })

    @classmethod
    def from_json(cls, string):
        """Create AnimeFiles from JSON string."""
        obj = json.loads(string)
        return cls(obj['regexp'], obj['files'])
