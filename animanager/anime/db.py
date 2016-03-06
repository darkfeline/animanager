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

from collections import namedtuple
import logging
import re
import sqlite3

from animanager import errors

logger = logging.getLogger(__name__)


class AnimeDB:

    """Our anime database."""

    VERSION = 1

    def __init__(self, path):
        self.dbfile = path
        self.connect()
        self._episode_types = None
        self.cache = sqlite3.connect(':memory:')
        self.cache.execute("""
        CREATE TABLE watched_episodes (
            aid INTEGER,
            number INTEGER,
            PRIMARY KEY (aid)
        )""")

    def connect(self):
        self.cnx = sqlite3.connect(self.dbfile)
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

    EpisodeType = namedtuple('EpisodeType', ['id', 'prefix'])

    @property
    def episode_types(self):
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

    Anime = namedtuple('Anime', ['aid', 'title', 'type', 'episodes',
                                 'watched_episodes'])

    def get_anime(self, aid):
        cur = self.cnx.execute("""
            SELECT aid, title, type, episode FROM anime
            WHERE aid = ?""", (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('aid provided does not exist')
        watched_episodes = self.cache.get_watched_episodes(aid)
        return self.Anime(*row, watched_episodes)

    def get_watched_episodes(self, aid):
        # Try to fetch from cache.
        cur = self.cache.execute("""
            SELECT number FROM watched_episodes
            WHERE aid = ?""", (aid,))
        row = cur.fetchone()
        if row is not None:
            return row[0]
        # Check if AID exists.
        cur = self.cnx.execute("""
            SELECT 1 FROM anime WHERE aid = ?
            """, (aid,))
        if cur.fetchone() is None:
            raise ValueError('aid provided does not exist')
        # We need to calculate watched_episodes.  We select the first regular episode that is
        # not watched.  Our watched_episodes is one less than that.
        cur = self.cnx.execute("""
            SELECT number FROM episode
            WHERE aid = ? AND user_watched = 0 AND type = ?
            ORDER BY number ASC
            LIMIT 1
            """, (aid, self.episode_types['regular']))
        row = cur.fetchone()
        if row is None:
            raise errors.DatabaseError('anime is missing episodes')
        episodes_watched = row[0] - 1
        # We store this in the cache.
        self.cache.execute("""
            INSERT OR REPLACE INTO watched_episodes
            (aid, number) VALUES (?, ?)
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
