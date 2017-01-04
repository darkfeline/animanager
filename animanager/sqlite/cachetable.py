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


class CacheTableManager:

    """CacheTable manager.

    Instances of this class manage cache table setup and cleanup.
    """

    def __init__(self, conn, tables: 'Iterable[CacheTable]'):
        self._conn = conn
        self._tables = tuple(tables)

    def setup(self):
        """Setup cache tables."""
        for table in self._tables:
            with self._conn:
                table.fsetup(self._conn)

    def teardown(self):
        """Cleanup cache tables."""
        for table in reversed(self._tables):
            with self._conn:
                table.fteardown(self._conn)


class CacheTable:

    """Cache table class.

    Instances of this class represent cache tables that can be added to
    :class:`~animanager.sqlite.db.SQLiteDB`.

    Instances need to define setup and cleanup functions via the
    :meth:`setup` and :meth:`cleanup` decorator methods.  The functions
    are called with a connection object.

    Setup functions should use ``IF NOT EXISTS`` to create tables.
    """

    def __init__(self, fsetup, fteardown):
        self.fsetup = fsetup
        self.fteardown = fteardown
