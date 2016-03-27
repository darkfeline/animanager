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

from abc import ABC, abstractmethod
from typing import Any, Iterable, Sequence

__all__ = ['BaseFiles']


class BaseFiles(ABC):

    """Interface for collections of files."""

    @abstractmethod
    def maybe_add(self, filename: str) -> None:
        pass

    @abstractmethod
    def maybe_add_iter(self, filenames: Iterable[str]) -> None:
        pass

    @abstractmethod
    def to_json(self):
        return '{}'

    @classmethod
    @abstractmethod
    def from_json(cls, string):
        return cls()


class BaseAnimeFiles(BaseFiles):

    @abstractmethod
    def available(self, episode: int) -> Any:
        """Return whether episode is available."""
        return False

    @abstractmethod
    def available_string(self, episode: int) -> str:
        """Return a string of available episodes.

        episode is the number of currently watched episodes, which is used to
        determine which episodes to display.

        """
        return ''

    @abstractmethod
    def get_episode(self, episode: int) -> Sequence[str]:
        return ()
