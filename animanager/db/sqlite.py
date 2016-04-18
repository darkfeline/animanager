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

        # Check database version.
        if self.version != self.required_version:
            raise DatabaseVersionError(self.required_version, self.version)

    @property
    def required_version(self):
        """Required database version.

        You should override this in subclasses.

        """
        return 0

    def connect(self, *args, **kwargs):
        """Connect to the database.

        This is called in :meth:`__init__`, so you should not call it yourself.

        """
        # pylint: disable=no-member
        self.cnx = apsw.Connection(*args, **kwargs)

    def cursor(self):
        """Get database cursor."""
        return self.cnx.cursor()

    def close(self):
        """Close the database connection."""
        self.cnx.close()

    def get_version(self):
        """Get database user version."""
        return self.cursor().execute('PRAGMA user_version').fetchone()[0]

    def set_version(self, version):
        """Set database user version."""
        # Parameterization doesn't work with PRAGMA, so we have to use string
        # formatting.  This is safe from injections because it coerces to int.
        return self.cursor().execute('PRAGMA user_version={:d}'.format(version))

    version = property(
        fget=get_version,
        fset=set_version,
        doc='SQLite database user version.')
