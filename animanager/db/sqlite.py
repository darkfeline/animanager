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

import apsw

from .errors import DatabaseVersionError


class SQLiteDB:

    """SQLite database for Animanager.

    SQLiteDB mixins that extend __init__() should call super().__init__()
    before running their own code, especially if they need access to the SQLite
    connection.  Mixins should therefore be included in reverse order:

        class Foo(SpamMixin, EggsMixin, SQLiteDB):

    This will run __init__() in order: SQLiteDB, EggsMixin, SpamMixin

    """

    def __init__(self, *args, **kwargs):
        self.connect(*args, **kwargs)
        version = get_version(self.cnx)
        if version != self.version:
            raise DatabaseVersionError(self.version, version)

    @property
    def version(self):
        """Required database version."""
        return 0

    def connect(self, *args, **kwargs):
        """Connect to the database.

        This is called in :meth:`__init__`, so you should not call it yourself.

        """
        # pylint: disable=no-member
        self.cnx = apsw.Connection(*args, **kwargs)

    def close(self):
        self.cnx.close()


def get_version(cnx):
    """Get SQLite database user version."""
    return cnx.cursor().execute('PRAGMA user_version').fetchone()[0]


def set_version(cnx, version):
    """Set SQLite database user version."""
    # Parameterization doesn't work with PRAGMA, so we have to use string
    # formatting.  This is safe from injections because it coerces to int.
    return cnx.cursor().execute('PRAGMA user_version={:d}'.format(version))
