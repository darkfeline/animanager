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

"""Tools for managing temporary cache tables in a SQLite database."""

from typing import Callable, List

from .db import SQLiteDB

CacheFunction = Callable[[SQLiteDB], None]


class CacheTableManager:

    """:class:`CacheTable` manager.

    Instances of this class manage cache table setup and cleanup on a
    :class:`SQLiteDB`.

    :param SQLiteDB database: database to bind to
    :param list tables: cache tables to use

    """

    def __init__(self, database: SQLiteDB, tables: List['CacheTable']):
        self.database = database
        for table in tables:
            if not isinstance(table, CacheTable):
                raise TypeError('{} is not a CacheTable'.format(table))
            if not table.is_complete:
                raise ValueError('{} is not completely defined'.format(table))
        self.tables = tuple(tables)

    def setup(self):
        """Setup cache tables."""
        for table in self.tables:
            with self.database:
                table.setup_func(self.database)

    def cleanup(self):
        """Cleanup cache tables."""
        for table in reversed(self.tables):
            with self.database:
                table.cleanup_func(self.database)


class CacheTable:

    """Cache table class.

    Instances of this class represent cache tables that can be added to
    :class:`~animanager.sqlite.db.SQLiteDB`.

    Instances need to define setup and cleanup functions via the :meth:`setup`
    and :meth:`cleanup` decorator methods.  The functions should take the
    :class:`~animanager.sqlite.db.SQLiteDB` as an argument.

    Setup functions should use ``IF NOT EXISTS`` to create tables.

    """

    def __init__(self):
        self.setup_func = None
        self.cleanup_func = None

    def setup(self, func: CacheFunction):
        """Decorator for setup function."""
        self.setup_func = func
        return func

    def cleanup(self, func: CacheFunction):
        """Decorator for cleanup function."""
        self.cleanup_func = func
        return func

    @property
    def is_complete(self):
        """Whether cache table is completely defined."""
        return self.setup_func is not None and self.cleanup_func is not None
