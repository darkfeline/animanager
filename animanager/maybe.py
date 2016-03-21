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

# pylint: disable=too-few-public-methods


def maybe(thing):
    if thing is None:
        return Nothing
    else:
        return Just(thing)


class Maybe(ABC):

    __slots__ = ()

    @abstractmethod
    def __bool__(self):
        pass

    @abstractmethod
    def get(self):
        pass


class Just(Maybe):

    __slots__ = ('thing',)

    def __init__(self, thing):
        self.thing = thing

    def __bool__(self):
        return True

    def get(self):
        return self.thing


class Nothing(Maybe):

    __slots__ = ()

    def __bool__(self):
        return False

    def get(self):
        raise TypeError('Nothing has nothing to get')
