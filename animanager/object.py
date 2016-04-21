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

"""Implementation of objects with fields.

Useful for implementing data bags, like a more flexible and powerful namedtuple
crossed with dict.

"""

from weakref import WeakKeyDictionary

# pylint: disable=too-few-public-methods


class Object:

    """Class that restricts instance attribute access.

    Used with :class:`Field`, can be used like an advanced namedtuple.

    >>> class Foo(Object):
    ...     bar = Field()
    ...
    >>> x = Foo()
    >>> x.bar = 2
    >>> x.bar
    2
    >>> del x.bar
    >>> x.bar
    Traceback (most recent call last):
        ...
    AttributeError: Field not set
    >>> del x.bar
    Traceback (most recent call last):
        ...
    AttributeError: Field not set
    >>> x.foo
    Traceback (most recent call last):
        ...
    AttributeError: No attribute foo

    Initial values can be passed to the instance constructor:

    >>> class Foo(Object):
    ...     bar = Field()
    ...
    >>> x = Foo(bar=2)
    >>> x.bar
    2

    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattribute__(self, name):
        try:
            descriptor = type(self).__dict__[name]
        except KeyError:
            raise AttributeError('No attribute {}'.format(name))
        else:
            return descriptor.__get__(self, type(self))

    def __setattr__(self, name, value):
        try:
            descriptor = type(self).__dict__[name]
        except KeyError:
            raise AttributeError('No attribute {}'.format(name))
        else:
            descriptor.__set__(self, value)

    def __delattr__(self, name):
        try:
            descriptor = type(self).__dict__[name]
        except KeyError:
            raise AttributeError('No attribute {}'.format(name))
        else:
            descriptor.__delete__(self)


class Field:

    """Transparent attribute descriptor."""

    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, obj, cls):
        if obj is None:
            return self
        try:
            return self.values[obj]
        except KeyError:
            raise AttributeError('Field not set')

    def __set__(self, obj, value):
        self.values[obj] = value

    def __delete__(self, obj):
        try:
            del self.values[obj]
        except KeyError:
            raise AttributeError('Field not set')
