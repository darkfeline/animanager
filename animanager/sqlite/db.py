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

"""SQLite database module."""

import logging

import apsw

logger = logging.getLogger(__name__)


class SQLiteDB:

    """This class encapsulates :class:`apsw.Connection` with useful helpers for
    foreign keys and user version.

    :class:`SQLiteDB` is not DB-API compatible, like :class:`apsw.Connection`.

    Database access is mainly handled through :meth:`cursor` and using
    :class:`SQLiteDB` as a context manager to control transactions:

    >>> db = SQLiteDB(':memory:')
    >>> with db:
    ...     cur = db.cursor()  # This is in a transaction.

    :meth:`__getattr__` has been overridden so :class:`apsw.Connection` methods
    can be accessed directly.

    """

    def __init__(self, *args, **kwargs):
        self.connect(*args, **kwargs)

    def __enter__(self):
        return self.cnx.__enter__()

    def __exit__(self, type, value, tb):
        # pylint: disable=redefined-builtin
        return self.cnx.__exit__(type, value, tb)

    def __getattr__(self, name):
        return getattr(self.cnx, name)

    def enable_foreign_keys(self):
        """Enable SQLite foreign key support."""
        cur = self.cursor()
        cur.execute('PRAGMA foreign_keys = 1')
        cur.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            raise SQLiteError('Foreign keys are not supported.')

    def disable_foreign_keys(self):
        """Disable SQLite foreign key support."""
        self.cursor().execute('PRAGMA foreign_keys = 0')

    def check_foreign_keys(self) -> list:
        """Check foreign keys for errors.

        :return: a list of errors
        :rtype: list

        """
        cur = self.cursor()
        cur.execute('PRAGMA foreign_key_check')
        return cur.fetchall()

    def connect(self, *args, **kwargs):
        """Connect to the database.

        This is called in :meth:`__init__`, so you do not need to call it
        yourself.

        """
        # pylint: disable=no-member
        self.cnx = apsw.Connection(*args, **kwargs)
        self.enable_foreign_keys()

    def get_version(self) -> int:
        """Get database user version."""
        return self.cursor().execute('PRAGMA user_version').fetchone()[0]

    def set_version(self, version: int) -> None:
        """Set database user version."""
        # Parameterization doesn't work with PRAGMA, so we have to use string
        # formatting.  This is safe from injections because it coerces to int.
        self.cursor().execute('PRAGMA user_version={:d}'.format(version))

    version = property(
        fget=get_version,
        fset=set_version,
        doc='SQLite database user version.')


class DatabaseError(Exception):
    """Generic database error."""


class SQLiteError(DatabaseError):
    """Database error caused by SQLite."""
