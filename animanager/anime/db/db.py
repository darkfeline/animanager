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

from animanager import errors

logger = logging.getLogger(__name__)


class AnimeDB:

    """Our anime database."""

    VERSION = 1

    def __init__(self, database):
        self.connect(database)
        self.cache = self.CacheDB()
        self._episode_types = None

    def connect(self, database):
        self.cnx = sqlite3.connect(database)
        cur = self.cnx.execute('PRAGMA user_version')
        version = cur.fetchone()[0]
        if version != self.VERSION:
            raise errors.DatabaseVersionError(self.VERSION, version)
        self.cnx.execute('PRAGMA foreign_keys = ON')
        cur = self.cnx.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            raise errors.DatabaseError('Foreign keys are not supported.')

    def close(self):
        self.cnx.close()
        self.cache.close()

    @property
    def episode_types(self):
        """Episode types.

        Returns a dictionary mapping episode type name strings to EpisodeType
        instances.  EpisodeType instances have two attributes, id and prefix.

        """
        if self._episode_types is None:
            self._episode_types = dict()
            cur = self.cnx.execute('SELECT id, name, prefix FROM episode_tupe')
            for type_id, name, prefix in cur:
                self._episode_types[name] = self.EpisodeType(type_id, prefix)
        return self._episode_types

    def add(self, anime):
        """Add an anime.

        anime is an AnimeTree instance.

        """
        self.cnx.execute("""
            INSERT INTO anime
            (aid, title, type, episodes, startdate, enddate)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (anime.aid, anime.title, anime.type, anime.episodecount,
             anime.startdate, anime.enddate))
        for episode in anime.episodes:
            self.cnx.execute("""
                INSERT INTO episode
                (anime, type, number, title, length, user_watched)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (anime.aid, episode.type, episode.number, episode.title,
                 episode.length, 0))
        self.cnx.commit()

    def get_anime(self, aid):
        """Get anime row from our permanent database.

        Returns AnimDB.Anime or raises ValueError.

        """
        cur = self.cnx.execute("""
            SELECT aid, title, type, episodes FROM anime
            WHERE aid = ?""", (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('aid provided does not exist')
        return self.Anime(*row)

    def get_anime_full(self, aid):
        """Get full anime row.

        This includes information that is not in the permanent database and
        will need to either be calculated or fetched from cache.

        """
        anime = self.get_anime(aid)
        status, watched_episodes = self.cache.get_watched_episodes(aid)
        return self.Anime(*row, status, watched_episodes)

    # XXX
    def get_anime_status(self, aid):
        """Get anime status.

        Returns a tuple (status, watched_episodes).  status is 1 or 0 depending
        on whether the anime is completed or not.

        """
        # Try to fetch from cache.
        try:
            return self.cache.get_anime_status(aid)
        except ValueError:
            pass
        # Check if anime exists.
        cur = self.cnx.execute("""
            SELECT episodes FROM anime WHERE aid = ?
            """, (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('aid provided does not exist')
        episodes = row[0]
        # We need to calculate status and watched_episodes.
        cur = self.cnx.execute("""
            SELECT number, user_watched FROM episode
            WHERE aid = ? AND type = ?
            ORDER BY number ASC
            """, (aid, self.episode_types['regular']))
        rows = cur.fetchall()
        if not rows:
            raise errors.DatabaseError('anime is missing episodes')
        # We find the last consecutive episode that is user_watched.
        for i, row in enumerate(rows):
            if row[1]:
        if not unwatched_rows:
        episodes_watched = row[0] - 1
        # We store this in the cache.
        self.cache.execute("""
            INSERT OR REPLACE INTO anime
            (aid, watched_episodes) VALUES (?, ?)
            """, (aid, episodes_watched))
        return episodes_watched

    class WatchingAnime:

        __slots__ = ['aid', 'regexp']

        def __init__(self, aid, regexp):
            self.aid = aid
            self.regexp = re.compile(regexp, re.I)

    def get_watching(self):
        """Return watching series."""
        cur = self.cnx.execute('SELECT aid, regexp FROM watching')
        return [self.WatchingAnime(aid, regexp)
                for aid, regexp in cur.fetchall()]
