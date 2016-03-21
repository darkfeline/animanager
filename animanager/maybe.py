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


class Maybe(ABC):

    __slots__ = ()

    @abstractmethod
    def has(self):
        pass

    @abstractmethod
    def get(self):
        pass


class Just(Maybe):

    __slots__ = ('thing',)

    def __init__(self, thing):
        self.thing = thing

    def has(self):
        return True

    def get(self):
        return self.thing


class Nothing(Maybe):

    __slots__ = ()

    def has(self):
        return False

    def get(self):
        return NullObject()


class NullObject:

    # pylint: disable=too-few-public-methods,no-self-use,unused-argument

    def __getattribute__(self, attr):
        return NullObject()

    def __call__(self, *args, **kwargs):
        return NullObject()

    def __repr__(self):
        return 'NullObject()'

    def __bytes__(self):
        return bytes()

    def __format__(self, format_spec):
        return 'NullObject()'

    def __lt__(self, other):
        return NullObject()

    def __le__(self, other):
        return NullObject()

    def __eq__(self, other):
        return NullObject()

    def __ne__(self, other):
        return NullObject()

    def __gt__(self, other):
        return NullObject()

    def __ge__(self, other):
        return NullObject()

    def __hash__(self):
        return 0

    def __len__(self):
        return 0

    def __setattr__(self, name, value):
        pass

    def __delattr__(self, name):
        pass

    def __getitem__(self, key):
        return NullObject()

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return iter(())

    def __contains__(self, item):
        return False

    def __add__(self, other):
        return NullObject()

    def __sub__(self, other):
        return NullObject()

    def __mul__(self, other):
        return NullObject()

    def __matmul__(self, other):
        return NullObject()

    def __truediv__(self, other):
        return NullObject()

    def __floordiv__(self, other):
        return NullObject()

    def __mod__(self, other):
        return NullObject()

    def __divmod__(self, other):
        return NullObject()

    def __pow__(self, other, modulo=None):
        return NullObject()

    def __lshift__(self, other):
        return NullObject()

    def __rshift__(self, other):
        return NullObject()

    def __and__(self, other):
        return NullObject()

    def __xor__(self, other):
        return NullObject()

    def __or__(self, other):
        return NullObject()

    def __radd__(self, other):
        return NullObject()

    def __rsub__(self, other):
        return NullObject()

    def __rmul__(self, other):
        return NullObject()

    def __rmatmul__(self, other):
        return NullObject()

    def __rtruediv__(self, other):
        return NullObject()

    def __rfloordiv__(self, other):
        return NullObject()

    def __rmod__(self, other):
        return NullObject()

    def __rdivmod__(self, other):
        return NullObject()

    def __rpow__(self, other):
        return NullObject()

    def __rlshift__(self, other):
        return NullObject()

    def __rrshift__(self, other):
        return NullObject()

    def __rand__(self, other):
        return NullObject()

    def __rxor__(self, other):
        return NullObject()

    def __ror__(self, other):
        return NullObject()

    def __iadd__(self, other):
        return NullObject()

    def __isub__(self, other):
        return NullObject()

    def __imul__(self, other):
        return NullObject()

    def __imatmul__(self, other):
        return NullObject()

    def __itruediv__(self, other):
        return NullObject()

    def __ifloordiv__(self, other):
        return NullObject()

    def __imod__(self, other):
        return NullObject()

    def __ipow__(self, other, modulo=None):
        return NullObject()

    def __ilshift__(self, other):
        return NullObject()

    def __irshift__(self, other):
        return NullObject()

    def __iand__(self, other):
        return NullObject()

    def __ixor__(self, other):
        return NullObject()

    def __ior__(self, other):
        return NullObject()

    def __neg__(self):
        return NullObject()

    def __pos__(self):
        return NullObject()

    def __abs__(self):
        return NullObject()

    def __invert__(self):
        return NullObject()

    def __complex__(self):
        return 0j

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __round__(self, n=None):
        return 0.0

    def __index__(self):
        return 0

    def __enter__(self):
        return NullObject()

    def __exit__(self, exc_type, exc_value, traceback):
        pass
