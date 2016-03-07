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

import weakref

from animanager.db import BaseCacheTableMixin
from animanager.db import BaseDispatcher

from .collections import AnimeStatus


class AnimeCacheMixin(BaseCacheTableMixin):

    def setup_cache_tables(self):
        self.cnx.execute("""
        CREATE TABLE IF NOT EXISTS cache_anime (
            aid INTEGER,
            complete INTEGER NOT NULL CHECK(status IN (0, 1)),
            watched_episodes INTEGER NOT NULL,
            PRIMARY KEY (aid),
            FOREIGN KEY (aid) REFERENCES anime(aid)
                ON DELETE CASCADE ON UPDATE CASCADE
        )""")
        super().setup_cache_tables()

    def cleanup_cache_tables(self):
        self.cnx.execute('DROP TABLE IF EXISTS cache_anime')
        super().cleanup_cache_tables()

    @property
    def anime_cache(self):
        return AnimeCacheDispatcher(self)


class AnimeCacheDispatcher(BaseDispatcher):

    __slots__ = ()

    def get_anime_status(self, aid):
        """Get anime status.

        Returns AnimeStatus or raises ValueError.

        """
        cur = self.cnx.execute("""
            SELECT complete, watched_episodes FROM cache_anime
            WHERE aid=?""", (aid,))
        if cur is None:
            raise ValueError('aid is not in cache')
        return AnimeStatus(aid, *cur)

    def set_anime_status(self, anime_status):
        """Set anime status."""
        self.cnx.execute(
            """INSERT OR REPLACE INTO cache_anime
            (aid, complete, watched_episodes)
            VALUES (?, ?, ?)""",
            anime_status)
        self.cnx.commit()
