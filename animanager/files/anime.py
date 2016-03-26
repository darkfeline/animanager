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

import json
import os
import re
from abc import abstractmethod
from collections import defaultdict
from typing import Dict, List, Sequence

from animanager.files import BaseFiles


def is_video(filepath):
    """Check filename extension to see if it's a video file."""
    extension = os.path.splitext(filepath)[1]
    return extension in ('.mkv', '.mp4', '.avi')


class BaseAnimeFiles(BaseFiles):

    @abstractmethod
    def available_string(self) -> str:
        return ''

    @abstractmethod
    def get_episode(self, episode: int) -> Sequence[str]:
        return ()


class FakeAnimeFiles(BaseAnimeFiles):

    """AnimeFiles null object.

    Should not be instantiated directly.

    """

    def maybe_add(self, filename):
        pass

    def maybe_add_iter(self, filenames):
        pass

    def available_string(self):
        return ''

    def get_episode(self, episode: int) -> Sequence[str]:
        return ()

    def to_json(self):
        return '{}'

    @classmethod
    def from_json(cls, string):
        return cls()


class AnimeFiles(BaseAnimeFiles):

    """Used for matching and grouping files for an anime."""

    def __new__(cls, regexp):
        if regexp:
            return super().__new__(cls)
        else:
            return FakeAnimeFiles()

    def __init__(self, regexp: str) -> None:
        self.regexp = re.compile(regexp)
        self.by_episode = defaultdict(list)  # type: Dict[int, List[str]]

    def maybe_add(self, filename):
        basename = os.path.basename(filename)
        match = self.regexp.search(basename)
        if match:
            self.by_episode[int(match.group('ep'))].append(filename)
            return True
        return False

    def maybe_add_iter(self, filenames):
        for filename in filenames:
            self.maybe_add(filename)

    def available_string(self):
        """Return a string of available episodes."""
        return ','.join(str(ep) for ep in sorted(self.by_episode.keys()))

    def get_episode(self, episode: int) -> List[str]:
        return self.by_episode[episode]

    def to_json(self):
        return json.dumps({
            'regexp': self.regexp.pattern,
            'by_episode': self.by_episode,
        })

    @classmethod
    def from_json(cls, string):
        obj = json.loads(string)
        if obj:
            anime_files = cls(obj['regexp'])
            anime_files.by_episode = defaultdict(
                list,
                ((int(ep), files) for ep, files in obj['by_episode'].items()),
            )
            return anime_files
        else:
            return FakeAnimeFiles()
