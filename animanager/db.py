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


class MigrationMixin(SQLiteDB):

    """Automated migration.

    Make sure to include this after UserVersionMixin.

    """
    def connect(self, database):
        super().connect(database)
        self.migrate(self.cnx)

    @abstractmethod
    def migrate(self, cnx):
        pass


class UserVersionMixin(SQLiteDB):

    """Enables SQLite database user version checking."""

    @property
    @abstractmethod
    def version(self):
        return 0

    def connect(self, database):
        super().connect(database)
        version = get_user_version(self.cnx)
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


def get_user_version(cnx):
    return cnx.execute('PRAGMA user_version').fetchone()[0]


def set_user_version(cnx, version):
    return cnx.execute('PRAGMA user_version = ?', (version,))


class MigrationManager:

    """Simple database migration manager."""

    def __init__(self, initial_version=0):
        self.migrations = dict()
        self.initial_version = initial_version
        self.current_version = initial_version

    def register(self, migration):
        """Register a migration for version.

        migration is a function taking a DB-API connection object that migrates
        the database from the previous version to the supplied version.

        You can only register migrations in order.  For example, you can
        register migrations from version 1 to 2, then 2 to 3, then 3 to 4.  You
        cannot register 1 to 2 followed by 3 to 4.  ValueError will be raised.

        """
        if migration.from_version != self.current_version:
            raise ValueError('cannot register disjoint migration')
        if migration.to_version <= migration.from_version:
            raise ValueError('migration must upgrade version')
        self.migrations[migration.from_version] = migration.from_version
        self.current_version = migration.to_version

    def migrate(self, cnx):
        """Migrate a database as needed.

        cnx is a DB-API connection object.  This is safe to call on an up to
        date database, on an old database, or an uninitialized database
        (version 0).

        """
        version = get_user_version(cnx)
        while version < self.current_version:
            try:
                migration = self.migrations[version]
            except KeyError:
                raise DatabaseMigrationError(
                    'no registered migration for database version')
            migration.migrate(cnx)
            version = migration.version
            set_user_version(cnx, version)


class BaseMigration(ABC):

    @property
    @abstractmethod
    def from_version(self):
        return 0

    @property
    @abstractmethod
    def to_version(self):
        return 0

    @abstractmethod
    def migrate(self, cnx):
        """Migrate a database to the current version.

        cnx is a DB-API connection object.

        """


class DatabaseError(Exception):
    """Database error."""


class DatabaseMigrationError(DatabaseError):
    """Database migration error."""


class DatabaseVersionError(DatabaseError):
    """Bad database version."""

    def __init__(self, wanted, found):
        self.wanted = wanted
        self.found = found

    def __str__(self):
        return 'Bad database version: wanted {}, found {}'.format(
            self.wanted, self.found)
