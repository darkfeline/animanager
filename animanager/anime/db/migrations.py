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

"""Migrations module.

Has one function, migrate(), for migrating AnimeDB databases.

"""

from animanager.db import MigrationManager
from animanager.db import BaseMigration

_manager = MigrationManager()


def _register(migration_class):
    _manager.register(migration_class())
    return migration_class


def migrate(cnx):
    _manager.migrate(cnx)


@_register
class Migration1(BaseMigration):

    @property
    def from_version(self):
        return 0

    @property
    def to_version(self):
        return 1

    def migrate(self, cnx):
        cnx.execute("""
        CREATE TABLE anime (
            aid INTEGER,
            title TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            episodes INTEGER,
            startdate DATE,
            enddate DATE,
            PRIMARY KEY (aid)
        )""")
        cnx.execute("""
        CREATE TABLE "episode" (
            id INTEGER,
            aid INTEGER NOT NULL,
            type INTEGER NOT NULL,
            number INTEGER NOT NULL,
            title TEXT NOT NULL,
            length INTEGER NOT NULL,
            user_watched INTEGER NOT NULL CHECK (user_watched IN (0, 1)),
            PRIMARY KEY (id),
            UNIQUE (aid, type, number),
            FOREIGN KEY (aid) REFERENCES anime (aid)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (type) REFERENCES episode_type (id)
                ON DELETE RESTRICT ON UPDATE CASCADE
        )""")
        cnx.execute("""
        CREATE TABLE episode_type (
            id INTEGER,
            name TEXT NOT NULL UNIQUE,
            prefix TEXT NOT NULL UNIQUE,
            PRIMARY KEY(id)
        )""")
        cnx.execute("""
        INSERT INTO episode_type
        (id, name, prefix)
        VALUES
        (1, 'regular', ''),
        (2, 'special', 'S'),
        (3, 'credit', 'C'),
        (4, 'trailer', 'T'),
        (5, 'parody', 'P'),
        (6, 'other', 'O')
        """)
        cnx.execute("""
        CREATE TABLE watching (
            aid INTEGER,
            regexp TEXT NOT NULL,
            PRIMARY KEY (aid),
            FOREIGN KEY (aid) REFERENCES anime (aid)
                ON DELETE CASCADE ON UPDATE CASCADE
        )""")
