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

import functools
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, TypeVar


class BaseCacheHolder(ABC):

    """Interface for objects that hold a cache."""

    @abstractmethod
    def purge_cache(self) -> None:
        pass


T = TypeVar('T')


def cached_property(func: Callable[[Any], T]) -> T:
    """Decorator implementing a cached property.

    Property can be cleared via descriptor protocol __delete__.

    """
    is_set = False
    cache = None  # type: Optional[T]
    @functools.wraps(func)
    def cache_wrapper(self):
        nonlocal cache, is_set
        if not is_set:
            cache = func(self)
            is_set = True
        return cache
    def clear_cache(self):
        nonlocal is_set
        is_set = False
    return property(cache_wrapper, None, clear_cache)
