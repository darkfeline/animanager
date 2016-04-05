# Copyright (C) 2016  Allen Li
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

__all__ = ['BaseCacheHolder']


class BaseCacheHolder(ABC):

    """Interface for objects that hold a cache."""

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def purge_cache(self) -> None:
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if any('purge_cache' in B.__dict__ for B in C.__mro__):
            return True
        return NotImplemented
