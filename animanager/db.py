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

from abc import ABC, abstractmethod
import sqlite3


class BaseDB(ABC):

    """Interface for database classes."""

    @abstractmethod
    def connect(self, database):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLiteDB(BaseDB):

    """SQLite database.

    Provides minimum functionality for SQLite connection.

    """

    def __init__(self, database):
        self.connect(database)

    def connect(self, database):
        self.cnx = sqlite3.connect(database)

    def close(self):
        self.cnx.close()


class ForeignKeyMixin(SQLiteDB):

    """Enables SQLite foreign key support."""

    def connect(self, database):
        super().connect(database)
        self.cnx.execute('PRAGMA foreign_keys = ON')
        cur = self.cnx.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            raise DatabaseError('Foreign keys are not supported.')


class UserVersionMixin(SQLiteDB):

    """Enables SQLite database user version checking."""

    @property
    @abstractmethod
    def version(self):
        return 0

    def connect(self, database):
        super().connect(database)
        cur = self.cnx.execute('PRAGMA user_version')
        version = cur.fetchone()[0]
        if version != self.version:
            raise DatabaseVersionError(self.version, version)


class BaseCacheTableMixin(BaseDB):

    """Interface for cache table mixins."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_cache_tables()

    @abstractmethod
    def setup_cache_tables(self):
        pass

    @abstractmethod
    def cleanup_cache_tables(self):
        pass


class BaseDispatcher:

    """Base class for dispatchers for BaseCacheTableMixin subclasses."""

    __slots__ = ('cnx',)

    def __init__(self, parent):
        self.cnx = parent.cnx


class DatabaseError(Exception):
    """Database error."""


class DatabaseVersionError(DatabaseError):
    """Bad database version."""

    def __init__(self, wanted, found):
        self.wanted = wanted
        self.found = found

    def __str__(self):
        return 'Bad database version: wanted {}, found {}'.format(
            self.wanted, self.found)
