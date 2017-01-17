# Copyright (C) 2015-2017  Allen Li
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

"""This module implements :class:`CachedView`."""

from abc import ABC, abstractmethod
from weakref import WeakKeyDictionary


class CachedView(ABC):

    """A cached view of a database.

    >>> from itertools import count
    >>> from apsw import Connection
    >>> db = Connection(':memory:')
    >>> class Foo(CachedView):
    ...     counter = count(1)
    ...     @classmethod
    ...     def _new_from_db(cls, db):
    ...         return next(cls.counter)
    ...
    >>> Foo.from_db(db)
    1
    >>> Foo.from_db(db)
    1
    >>> Foo.forget(db)
    >>> Foo.from_db(db)
    2

    """

    _cache = WeakKeyDictionary()

    @classmethod
    @abstractmethod
    def _new_from_db(cls, db):
        """Make a new instance from a database.

        This should not be called directly; use :meth:`from_db`

        Subclasses should implement this.

        """

    @classmethod
    def from_db(cls, db, force=False):
        """Make instance from database.

        For performance, this caches the episode types for the database.  The
        `force` parameter can be used to bypass this.

        """
        if force or db not in cls._cache:
            cls._cache[db] = cls._new_from_db(db)
        return cls._cache[db]

    @classmethod
    def forget(cls, db):
        """Forget cache for database."""
        cls._cache.pop(db, None)
