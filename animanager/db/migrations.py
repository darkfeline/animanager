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

import logging
from abc import ABC, abstractmethod

from animanager.db import DatabaseError

from .sqlite import SQLiteDB
from .versions import get_user_version, set_user_version

logger = logging.getLogger(__name__)


class MigrationMixin(SQLiteDB):

    """Automated migration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.migrate()

    @property
    @abstractmethod
    def migration_manager(self):
        pass

    def needs_migration(self):
        """Check if database needs migration."""
        return self.migration_manager.needs_migration(self.cnx)

    def migrate(self):
        self.migration_manager.migrate(self.cnx)


class MigrationManager:

    """Simple database migration manager."""

    def __init__(self, initial_version=0):
        self.migrations = dict()
        self.initial_version = initial_version
        self.current_version = initial_version

    def register(self, migration: 'BaseMigration') -> None:
        """Register a migration.

        You can only register migrations in order.  For example, you can
        register migrations from version 1 to 2, then 2 to 3, then 3 to 4.  You
        cannot register 1 to 2 followed by 3 to 4.  ValueError will be raised.

        """
        if not isinstance(migration, BaseMigration):
            raise TypeError('migration must be a BaseMigration instance')
        if migration.from_version != self.current_version:
            raise ValueError('cannot register disjoint migration')
        if migration.to_version <= migration.from_version:
            raise ValueError('migration must upgrade version')
        self.migrations[migration.from_version] = migration
        self.current_version = migration.to_version

    def needs_migration(self, cnx):
        """Check if database needs migration."""
        return get_user_version(cnx) < self.current_version

    def migrate_single(self, cnx, version: int) -> int:
        """Perform a single migration starting from given version.

        Returns the version after migration.

        """
        with cnx:
            try:
                migration = self.migrations[version]
            except KeyError:
                raise DatabaseMigrationError(
                    'no registered migration for database version')
            logger.info('Migrating database from %d to %d',
                        migration.from_version, migration.to_version)
            migration.migrate(cnx)
            version = migration.to_version
            set_user_version(cnx, version)
            return version

    def migrate(self, cnx):
        """Migrate a database as needed.

        This is safe to call on an up to date database, on an old database, or
        an uninitialized database (version 0).

        """
        version = get_user_version(cnx)
        while version < self.current_version:
            version = self.migrate_single(cnx, version)


class BaseMigration(ABC):

    """Base Migration class.

    Subclasses define database migrations from one version to another version.
    Migration subclasses should not commit their transaction nor increment the
    database user version; the MigrationManager handles that.

    """

    _from_version = 0
    _to_version = 0

    @property
    def from_version(self):
        return self._from_version

    @property
    def to_version(self):
        return self._to_version

    @staticmethod
    @abstractmethod
    def migrate(cnx):
        """Migrate a database to the current version.

        cnx is a DB-API connection object.

        """


def migration(from_version, to_version):
    """Migration decorator."""
    def decorate(func):
        return make_migration(from_version, to_version, func)
    return decorate


def make_migration(from_version, to_version, migrate_func):
    """Make BaseMigration subclass dynamically."""
    return type(
        'M{}'.format(to_version),
        (BaseMigration,),
        {
            '_from_version': from_version,
            '_to_version': to_version,
            'migrate': staticmethod(migrate_func),
        })


class DatabaseMigrationError(DatabaseError):
    """Database migration error."""
