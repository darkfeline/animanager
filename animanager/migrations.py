# Copyright (C) 2016, 2017  Allen Li
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

Members:

manager
"""

import datetime
import logging
import shutil
import sqlite3

from mir import sqlite3m

from animanager import datets

logger = logging.getLogger(__name__)


def migrate(path: str):
    conn = sqlite3.connect(path)
    if manager.should_migrate(conn):
        logger.info('Migration needed, backing up database')
        shutil.copyfile(path, path + '~')
        logger.info('Migrating database')
        manager.migrate(conn)
    conn.close()


manager = sqlite3m.MigrationManager()
manager.register_wrapper(sqlite3m.CheckForeignKeysWrapper)


@manager.migration(0, 1)
def _migrate1(conn):
    conn.execute("""\
    CREATE TABLE anime (
        aid INTEGER,
        title TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        episodes INTEGER,
        startdate DATE,
        enddate DATE,
        PRIMARY KEY (aid)
    )""")
    conn.execute("""\
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
    conn.execute("""\
    CREATE TABLE episode_type (
        id INTEGER,
        name TEXT NOT NULL UNIQUE,
        prefix TEXT NOT NULL UNIQUE,
        PRIMARY KEY(id)
    )""")
    conn.execute("""\
    CREATE TABLE watching (
        aid INTEGER,
        regexp TEXT NOT NULL,
        PRIMARY KEY (aid),
        FOREIGN KEY (aid) REFERENCES anime (aid)
            ON DELETE CASCADE ON UPDATE CASCADE
    )""")
    with conn:
        conn.execute("""\
        INSERT INTO episode_type (id, name, prefix) VALUES
        (1, 'regular', ''),
        (2, 'special', 'S'),
        (3, 'credit', 'C'),
        (4, 'trailer', 'T'),
        (5, 'parody', 'P'),
        (6, 'other', 'O')""")


@manager.migration(1, 2)
def _migrate2(conn):
    # Alter anime.
    conn.execute("""\
    CREATE TABLE anime_new (
        aid INTEGER,
        title TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        episodecount INTEGER NOT NULL,
        startdate INTEGER,
        enddate INTEGER,
        PRIMARY KEY (aid)
    )""")

    with conn:
        conn.execute("""\
        INSERT INTO anime_new (aid, title, type, episodecount)
        SELECT aid, title, type, episodes
        FROM anime""")
        # This is done in Python instead of SQL because fuck timezones.
        result = conn.execute('SELECT aid, startdate, enddate FROM anime')
        conn.executemany(
            """\
            UPDATE anime_new
            SET startdate=?, enddate=?
            WHERE aid=?""",
            ([datets.to_ts(_parse_date(startdate)) if startdate else None,
              datets.to_ts(_parse_date(enddate)) if enddate else None,
              aid]
             for aid, startdate, enddate in result),
        )
    conn.execute('DROP TABLE anime')
    conn.execute('ALTER TABLE anime_new RENAME TO anime')

    # Add title index.
    conn.execute("""\
    CREATE INDEX anime_titles ON anime (title)
    """)

    # Add file_priority.
    conn.execute("""\
    CREATE TABLE file_priority (
        id INTEGER PRIMARY KEY,
        regexp TEXT NOT NULL,
        priority INTEGER NOT NULL
    )""")


@manager.migration(2, 3)
def _migrate3(conn):
    # Alter anime.
    conn.execute("""\
    CREATE TABLE episode_new (
        id INTEGER,
        aid INTEGER NOT NULL,
        type INTEGER NOT NULL,
        number INTEGER NOT NULL,
        title TEXT NOT NULL,
        length INTEGER NOT NULL,
        user_watched INTEGER NOT NULL CHECK (user_watched IN (0, 1))
            DEFAULT 0,
        PRIMARY KEY (id),
        UNIQUE (aid, type, number),
        FOREIGN KEY (aid) REFERENCES anime (aid)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (type) REFERENCES episode_type (id)
            ON DELETE RESTRICT ON UPDATE CASCADE
    )""")
    with conn:
        conn.execute("""\
        INSERT INTO episode_new
        (id, aid, type, number, title, length, user_watched)
        SELECT id, aid, type, number, title, length, user_watched
        FROM episode
        """)
    conn.execute('DROP TABLE episode')
    conn.execute('ALTER TABLE episode_new RENAME TO episode')


def _parse_date(string: str) -> datetime.date:
    """Parse an ISO format date (YYYY-mm-dd).

    >>> _parse_date('1990-01-02')
    datetime.date(1990, 1, 2)
    """
    return datetime.datetime.strptime(string, '%Y-%m-%d').date()
