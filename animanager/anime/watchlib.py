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

from abc import ABC
from abc import abstractmethod
from collections import defaultdict
import os
import re


def is_video(filename):
    """Check filename extension to see if it's a video file."""
    extension = os.path.splitext(filename)[1]
    return extension in ('.mkv', '.mp4', '.avi')


def find_files(dirpath):
    """Find all video files.

    Returns a generator that yields paths in no particular order.

    """
    for dirpath, _, filenames in os.walk(dirpath):
        for filename in filenames:
            if is_video(filename):
                yield os.path.join(dirpath, filename)


class BaseAnimeFiles(ABC):

    """Interface for AnimeFiles."""

    @abstractmethod
    def maybe_add(self, filename):
        pass

    @abstractmethod
    def maybe_add_iter(self, filenames):
        pass

    @abstractmethod
    def available_string(self):
        return ''


class FakeAnimeFiles(BaseAnimeFiles):

    """Fake AnimeFiles to return to avoid the OOP NULL."""

    def maybe_add(self, filename):
        pass

    def maybe_add_iter(self, filenames):
        pass

    def available_string(self):
        return ''


class AnimeFiles(BaseAnimeFiles):

    """Used for matching and grouping files for an anime.

    Use the animefiles() module function instead of instantiating directly.

    """

    def __init__(self, regexp):
        self.regexp = re.compile(regexp)
        self.by_episode = defaultdict(list)

    def maybe_add(self, filename):
        basename = os.path.basename(filename)
        match = self.regexp.search(basename)
        if match:
            self.by_episode[int(match.ep)].append(filename)
            return True
        return False

    def maybe_add_iter(self, filenames):
        for filename in filenames:
            self.maybe_add(filename)

    def available_string(self):
        """Return a string of available episodes."""
        return ','.join(sorted(self.by_episode.keys()))


def animefiles(regexp):
    if regexp is None:
        return FakeAnimeFiles()
    else:
        return AnimeFiles(regexp)
