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

from abc import abstractmethod

from animanager.db import DatabaseError

from .sqlite import SQLiteDB


class UserVersionMixin(SQLiteDB):

    """Enables SQLite database user version checking."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        version = get_user_version(self.cnx)
        if version != self.version:
            raise DatabaseVersionError(self.version, version)

    @property
    @abstractmethod
    def version(self):
        return 0


def get_user_version(cnx):
    return cnx.cursor().execute('PRAGMA user_version').fetchone()[0]


def set_user_version(cnx, version):
    # Parameterization doesn't work with PRAGMA.  This should still be safe
    # from injections and such.
    return cnx.cursor().execute('PRAGMA user_version={:d}'.format(version))


class DatabaseVersionError(DatabaseError):
    """Bad database version."""

    def __init__(self, wanted, found):
        self.wanted = wanted
        self.found = found

    def __str__(self):
        return 'Bad database version: wanted {}, found {}'.format(
            self.wanted, self.found)
