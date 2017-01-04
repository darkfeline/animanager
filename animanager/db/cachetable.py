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

"""Animanager database cache tables."""

from animanager.sqlite import CacheTableSpec, CacheTableManager


def make_manager(conn):
    """Make CacheTableManager."""
    return CacheTableManager(conn, [_anime_cache])


def _setup(conn):
    """CacheTable setup function."""
    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS cache_anime (
        aid INTEGER,
        complete INTEGER NOT NULL CHECK(complete IN (0, 1)),
        watched_episodes INTEGER NOT NULL,
        anime_files TEXT,
        PRIMARY KEY (aid),
        FOREIGN KEY (aid) REFERENCES anime(aid)
            ON DELETE CASCADE ON UPDATE CASCADE
    )""")


def _teardown(conn):
    """CacheTable teardown function."""
    conn.cursor().execute('DROP TABLE IF EXISTS cache_anime')


_anime_cache = CacheTableSpec(_setup, _teardown)
