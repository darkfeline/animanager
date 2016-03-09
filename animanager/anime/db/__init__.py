# Copyright (C) 2015-2016  Allen Li
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
import re
import sqlite3

from animanager import db

from .cache import AnimeCacheMixin
from . import migrations
from .collections import EpisodeType
from .collections import Anime
from .collections import AnimeFull
from .collections import AnimeStatus
from .collections import WatchingAnime

logger = logging.getLogger(__name__)


class AnimeDB(
        AnimeCacheMixin, db.UserVersionMixin, db.ForeignKeyMixin, db.MigrationMixin
): # pylint: disable=too-many-ancestors

    """Our anime database."""

    def __init__(self, database):
        super().__init__(database)
        self._episode_types = None

    @property
    def version(self):
        return 1

    def migrate(self, cnx):
        migrations.migrate(cnx)

    @property
    def episode_types(self):
        """Episode types.

        Returns a dictionary mapping episode type name strings to EpisodeType
        instances.  EpisodeType instances have two attributes, id and prefix.

        """
        if self._episode_types is None:
            self._episode_types = dict()
            cur = self.cnx.execute('SELECT id, name, prefix FROM episode_type')
            for type_id, name, prefix in cur:
                self._episode_types[name] = EpisodeType(type_id, prefix)
        return self._episode_types

    def add(self, anime):
        """Add an anime (or update existing).

        anime is an AnimeTree instance.

        """
        self.cnx.execute(
            """INSERT OR REPLACE INTO anime
            (aid, title, type, episodes, startdate, enddate)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (anime.aid, anime.title, anime.type, anime.episodecount,
             anime.startdate, anime.enddate))
        for episode in anime.episodes:
            cur = self.cnx.execute(
                """INSERT OR IGNORE INTO episode
                (aid, type, number, title, length, user_watched)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (anime.aid, episode.type, episode.number, episode.title,
                 episode.length, 0))
            if cur.rowcount == 0:
                self.cnx.execute(
                    """UPDATE episode
                    SET title=:title, length=:length
                    WHERE aid=:aid AND type=:type AND number=:number""",
                    {
                        'aid': anime.aid,
                        'type': episode.type,
                        'number': episode.number,
                        'title': episode.title,
                        'length': episode.length,
                    })
        self.cnx.commit()

    def bump(self, aid):
        """Bump anime regular episode count."""
        anime_full = self.get_anime_full(aid)
        if anime_full.complete:
            return
        episode = anime_full.watched_episodes + 1
        self.cnx.execute(
            """UPDATE episode SET user_watched=:watched
            WHERE aid=:aid AND type=:type AND number=:number""",
            {
                'aid': aid,
                'type': self.episode_types['regular'].id,
                'number': episode,
                'watched': 1,
            })
        self.cnx.commit()
        self.anime_cache.set_anime_status(
            AnimeStatus(aid, episode >= anime_full.episodes, episode))

    def search_anime(self, query):
        """Perform a LIKE title search on the anime table.

        Returns an Anime instance generator.

        """
        cur = self.cnx.execute("""
            SELECT aid, title, type, episodes, startdate, enddate
            FROM anime WHERE title LIKE ?
            """, (query,))
        for row in cur:
            yield Anime(*row)

    def get_anime(self, aid):
        """Get anime row from our permanent database.

        Returns an Anime instance or raises ValueError.

        """
        cur = self.cnx.execute("""
            SELECT aid, title, type, episodes, startdate, enddate
            FROM anime
            WHERE aid = ?""", (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('aid provided does not exist')
        return Anime(*row)

    def get_anime_status(self, aid):
        """Get anime status.

        Returns an AnimeStatus instance or raises ValueError.  Anime status
        information is non-canonical and must be calculated or retrieved from
        cache.

        """

        # Try to fetch from cache.
        try:
            return self.anime_cache.get_anime_status(aid)
        except ValueError:
            pass

        # Check if anime exists.
        cur = self.cnx.execute("""
            SELECT episodes FROM anime WHERE aid=?
            """, (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('aid provided does not exist')
        episodes = row[0]

        # Select all regular episodes in ascending order.
        cur = self.cnx.execute("""
            SELECT number, user_watched FROM episode
            WHERE aid=? AND type=?
            ORDER BY number ASC
            """, (aid, self.episode_types['regular'].id))
        rows = cur.fetchall()
        if not rows:
            raise db.DatabaseError('anime is missing episodes')

        # We find the last consecutive episode that is user_watched.
        number = 0
        for number, watched in rows:
            # Once we find the first unwatched episode, we set the last
            # consecutive watched episode to the previous episode (or 0).
            if watched == 0:
                number -= 1
                break
        # We store this in the cache.
        anime_status = AnimeStatus(aid, episodes <= number, number)
        self.anime_cache.set_anime_status(anime_status)
        return anime_status

    def get_watching(self):
        """Return watching series."""
        cur = self.cnx.execute('SELECT aid, regexp FROM watching')
        return [WatchingAnime(aid, re.compile(regexp, re.I))
                for aid, regexp in cur.fetchall()]
