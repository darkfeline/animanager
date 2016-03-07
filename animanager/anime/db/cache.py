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

import sqlite3

from .collections import AnimeStatus


class CacheDB:

    def __init__(self):
        self.cnx = sqlite3.connect(':memory:')
        self.cnx.execute("""
        CREATE TABLE anime (
            aid INTEGER,
            status INTEGER NOT NULL CHECK(status IN (0, 1)),
            watched_episodes INTEGER NOT NULL,
            PRIMARY KEY (aid)
        )""")

    def close(self):
        self.cnx.close()

    def get_anime_status(self, aid):
        """Try to get anime status from cache.

        Returns a tuple (status, watched_episodes).  If AID is not in cache,
        raises ValueError.

        """
        cur = self.cnx.execute("""
            SELECT status, watched_episodes FROM anime
            WHERE aid = ?""", (aid,))
        row = cur.fetchone()
        if row is not None:
            return AnimeStatus(aid, *row)
        else:
            raise ValueError('AID not in cache database')

    def set_anime_status(self, anime_status):
        """Set anime status."""
        self.cnx.execute("""
            INSERT OR REPLACE INTO anime
            (aid, status, watched_episodes)
            VALUES (?, ?, ?)
            """, anime_status)
