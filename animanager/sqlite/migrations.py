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

"""Simple SQLite migration features."""

import logging
from typing import Callable

from .db import DatabaseError, SQLiteDB

logger = logging.getLogger(__name__)

MigrationFunction = Callable[[SQLiteDB], None]


class MigrationManager:

    """Simple database migration manager.

    This is used to set up database migrations and is then injected into
    :class:`SQLiteDB`.

    .. attribute:: initial_ver

       Starting version supported by manager.

    .. attribute:: final_ver

       Final version supported by manager.

    """

    def __init__(self, initial_ver=0):
        self.migrations = dict()
        self.initial_ver = self.final_ver = initial_ver

    def register(self, migration: 'Migration') -> None:
        """Register a migration.

        You can only register migrations in order.  For example, you can
        register migrations from version 1 to 2, then 2 to 3, then 3 to 4.  You
        cannot register 1 to 2 followed by 3 to 4.

        :raises TypeError: argument is not an instance of :class:`Migration`
        :raises ValueError: something is wrong with the migration

        """
        if not isinstance(migration, Migration):
            raise TypeError('migration must be a Migration instance')
        if migration.from_ver != self.final_ver:
            raise ValueError('cannot register disjoint migration')
        if migration.to_ver <= migration.from_ver:
            raise ValueError('migration must upgrade version')
        self.migrations[migration.from_ver] = migration
        self.final_ver = migration.to_ver

    def migration(self, from_ver: int, to_ver: int) -> \
        Callable[[MigrationFunction], 'Migration']:
        """Function decorator to create a migration and register it.

        >>> manager = MigrationManager()
        >>> @manager.migration(0, 1)
        ... def migrate(database):
        ...     pass

        """
        def decorate(func):
            """Decorator."""
            migration = Migration(from_ver, to_ver, func)
            self.register(migration)
            return migration
        return decorate

    def needs_migration(self, database) -> bool:
        """Check if database needs migration."""
        return database.version < self.final_ver

    def check_version(self, database):
        """Check database version.

        :raises VersionError: database does not satisfy final migration version

        """
        if database.version != self.final_ver:
            raise VersionError(self.final_ver, database.version)

    def migrate_single(self, database):
        """Perform a single migration starting from given version.

        Returns the version after migration.

        """
        database.disable_foreign_keys()
        with database:
            version = database.version
            if version not in self.migrations:
                raise MigrationError('No registered migration for database version')
            migration = self.migrations[version]
            logger.info('Migrating database from %d to %d',
                        migration.from_ver, migration.to_ver)
            migration.migrate(database)
            foreign_key_errors = database.check_foreign_keys()
            if foreign_key_errors:
                raise MigrationError(
                    'Foreign key check failed: %r',
                    foreign_key_errors)
            database.version = migration.to_ver
        database.enable_foreign_keys()

    def migrate(self, database):
        """Migrate a database as needed.

        This method is safe to call on an up to date database, on an old
        database, or an uninitialized database (version 0).

        This method is idempotent.

        :param database: database to migrate
        :type database: SQLiteDB

        """
        while database.version < self.final_ver:
            self.migrate_single(database)


class Migration(tuple):

    """Migration representing a single migration specification.

    :param int from_ver: version before migration
    :param int to_ver: version after migration
    :param callable migrate_func: a function taking a DB-API connection object

    """

    __slots__ = []

    def __new__(cls, from_ver, to_ver, migrate_func):
        return super().__new__(cls, (from_ver, to_ver, migrate_func))

    @property
    def from_ver(self):
        """Version before migration."""
        return self[0]

    @property
    def to_ver(self):
        """Version after migration."""
        return self[1]

    @property
    def migrate(self):
        """Migration function."""
        return self[2]


class MigrationError(DatabaseError):
    """Migration error."""


class VersionError(DatabaseError):

    """Bad database version."""

    def __init__(self, wanted, found):
        self.wanted = wanted
        self.found = found
        super().__init__('Bad database version: wanted {}, found {}'.format(
            self.wanted, self.found))
