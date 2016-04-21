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

from weakref import WeakKeyDictionary


class CachedProperty:

    """Descriptor implementing a cached property."""

    # pylint: disable=too-few-public-methods

    def __init__(self, func):
        self.cache = WeakKeyDictionary()
        self.func = func

    def __get__(self, obj, owner):
        if obj is None:
            return self
        if obj not in self.cache:
            self.cache[obj] = self.func(obj)
        return self.cache[obj]

    def __set__(self, obj, value):
        raise AttributeError('Cannot set value on CachedProperty')

    def __delete__(self, obj):
        self.cache.pop(obj, None)


def cached_property(func):
    """Cached property decorator."""
    return CachedProperty(func)
