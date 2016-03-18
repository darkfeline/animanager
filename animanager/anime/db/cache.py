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

from animanager.db import BaseCacheTableMixin
from animanager.db import BaseDispatcher

from .collections import AnimeStatus


class AnimeCacheMixin(BaseCacheTableMixin):

    def setup_cache_tables(self):
        self.cnx.cursor().execute("""
        CREATE TABLE IF NOT EXISTS cache_anime (
            aid INTEGER,
            complete INTEGER NOT NULL CHECK(complete IN (0, 1)),
            watched_episodes INTEGER NOT NULL,
            anime_files PICKLE,
            PRIMARY KEY (aid),
            FOREIGN KEY (aid) REFERENCES anime(aid)
                ON DELETE CASCADE ON UPDATE CASCADE
        )""")
        super().setup_cache_tables()

    def cleanup_cache_tables(self):
        self.cnx.cursor().execute('DROP TABLE IF EXISTS cache_anime')
        super().cleanup_cache_tables()

    @property
    def anime_cache(self):
        return AnimeCacheDispatcher(self)


class AnimeCacheDispatcher(BaseDispatcher):

    __slots__ = ()

    def set_status(self, anime_status):
        """Set anime status."""
        if not isinstance(anime_status, AnimeStatus):
            raise TypeError('anime_status must be an instance of AnimeStatus')
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """UPDATE cache_anime
                SET complete=?, watched_episodes=?
                WHERE aid=?""",
                (anime_status.complete,
                 anime_status.watched_episodes,
                 anime_status.aid))
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT OR IGNORE INTO cache_anime
                    (aid, complete, watched_episodes)
                    VALUES (?, ?, ?)""",
                    anime_status)
