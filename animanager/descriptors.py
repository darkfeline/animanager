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

    """Descriptor implementing a cached property.

    >>> from itertools import count
    >>> class Foo:
    ...     def __init__(self):
    ...         self.count = count(1)
    ...     def _foo(self):
    ...         return next(self.count)
    ...     foo = CachedProperty(_foo)
    ...
    >>> x = Foo()
    >>> x.foo
    1
    >>> x.foo
    1
    >>> del x.foo
    >>> x.foo
    2

    """

    def __init__(self, fget):
        self.cache = WeakKeyDictionary()
        self.fget = fget

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if instance not in self.cache:
            self.cache[instance] = self.fget(instance)
        return self.cache[instance]

    def __set__(self, instance, value):
        raise AttributeError('Cannot set value on CachedProperty')

    def __delete__(self, instance):
        self.cache.pop(instance, None)
