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
import shutil

from animanager.date import timestamp
import animanager.db.sqlite
import animanager.db.fk
import animanager.db.migrations
import animanager.db.versions

from .cache import AnimeCacheMixin
from .collections import EpisodeType
from .collections import Anime
from .collections import AnimeFull
from .collections import Episode
from .collections import AnimeStatus
from .migrations import migrations_list

logger = logging.getLogger(__name__)


class AnimeDB(
        AnimeCacheMixin,
        animanager.db.versions.UserVersionMixin,
        animanager.db.migrations.MigrationMixin,
        animanager.db.fk.ForeignKeyMixin,
        animanager.db.sqlite.SQLiteDB,
): # pylint: disable=too-many-ancestors

    """Our anime database."""

    def __init__(self, database):
        self.database = database
        super().__init__(database)
        self._episode_types = None
        self._episode_types_by_id = None

    @property
    def version(self):
        return self.migration_manager.current_version

    @property
    def migration_manager(self):
        try:
            manager = self._migration_manager
        except AttributeError:
            manager = animanager.db.fk.MigrationManager()
            for migration_class in migrations_list:
                manager.register(migration_class())
            self._migration_manager = manager
        return manager

    def migrate(self):
        if self.needs_migration():
            logger.info('Migration needed, backing up database')
            shutil.copyfile(self.database, self.database + '~')
            logger.info('Migrating database')
            super().migrate()

    @property
    def episode_types(self):
        """Episode types.

        Returns a dictionary mapping episode type name strings to EpisodeType
        instances.

        """
        if self._episode_types is None:
            ep_types = dict()
            cur = self.cnx.cursor()
            cur.execute('SELECT id, name, prefix FROM episode_type')
            for type_id, name, prefix in cur:
                ep_types[name] = EpisodeType(type_id, prefix)
            self._episode_types = ep_types
        return self._episode_types

    @property
    def episode_types_by_id(self):
        """Episode types by id.

        Returns a dictionary mapping episode type ids to EpisodeType
        instances.

        """
        if self._episode_types_by_id is None:
            ep_types = dict()
            cur = self.cnx.cursor()
            cur.execute('SELECT id, prefix FROM episode_type')
            for type_id, prefix in cur:
                ep_types[type_id] = EpisodeType(type_id, prefix)
            self._episode_types_by_id = ep_types
        return self._episode_types_by_id

    def get_epno(self, episode):
        """Return epno for Episode instance.

        epno is a string formatted with the episode number and type,
        e.g., S1, T2.

        """
        return '{}{}'.format(self.episode_types_by_id[episode.type].prefix,
                             episode.number)

    def add(self, anime):
        """Add an anime (or update existing).

        anime is an AnimeTree instance.

        """
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """INSERT OR REPLACE INTO anime (
                    aid,
                    title,
                    type,
                    episodecount,
                    startdate,
                    enddate)
                VALUES (
                    :aid,
                    :title,
                    :type,
                    :episodecount,
                    :startdate,
                    :enddate)""",
                {
                    'aid': anime.aid,
                    'title': anime.title,
                    'type': anime.type,
                    'episodecount': anime.episodecount,
                    'startdate': timestamp(anime.startdate),
                    'enddate': timestamp(anime.enddate),
                })
            for episode in anime.episodes:
                self.add_episode(anime.aid, episode)

    def add_episode(self, aid, episode):
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """UPDATE episode
                SET title=:title, length=:length
                WHERE aid=:aid AND type=:type AND number=:number""",
                {
                    'aid': aid,
                    'type': episode.type,
                    'number': episode.number,
                    'title': episode.title,
                    'length': episode.length,
                })
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT INTO episode (
                        aid,
                        type,
                        number,
                        title,
                        length,
                        user_watched)
                    VALUES (
                        :aid,
                        :type,
                        :number,
                        :title,
                        :length,
                        :user_watched)""",
                    {
                        'aid': aid,
                        'type': episode.type,
                        'number': episode.number,
                        'title': episode.title,
                        'length': episode.length,
                        'user-watched': 0,
                    })

    def search(self, query):
        """Perform a LIKE title search on the anime table.

        Returns an Anime instance generator.  Caches anime status lazily.

        """
        aids = self.cnx.cursor()
        aids.execute('SELECT aid FROM anime WHERE title LIKE ?', (query,))
        for aid in aids:
            aid = aid[0]
            self.cache_status(aid)
            cur = self.cnx.cursor()
            cur.execute("""
                SELECT anime.aid, title, type, episodecount,
                    watched_episodes, complete, regexp
                FROM anime JOIN cache_anime USING (aid)
                LEFT JOIN watching USING (aid)
                WHERE anime.aid=?""", (aid,))
            yield Anime(*cur.fetchone())

    def lookup_title(self, aid):
        """Look up anime title."""
        cur = self.cnx.cursor()
        cur.execute('SELECT title FROM anime WHERE aid=?', (aid,))
        anime = cur.fetchone()
        if anime is None:
            raise ValueError('Invalid aid')
        return anime[0]

    def lookup(self, aid, episodes=False):
        """Look up full information for a single anime.

        If episodes is True, individual episodes will be looked up and included
        in the returned AnimeFull instance.  Otherwise, the episodes attribute
        on the returned AnimeFull instance will be None.

        This forces status calculation.

        """
        self.cache_status(aid, force=True)
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute("""
                SELECT anime.aid, title, type, episodecount,
                    startdate, enddate,
                    watched_episodes, complete,
                    regexp
                FROM anime
                    JOIN cache_anime USING (aid)
                    LEFT JOIN watching USING (aid)
                WHERE anime.aid=?""", (aid,))
            anime = cur.fetchone()
            if anime is None:
                raise ValueError('Invalid aid')
            if episodes:
                cur.execute("""
                    SELECT aid, type, number, title, length, user_watched
                    FROM episode WHERE aid=?""", (aid,))
                episodes = [Episode(*row) for row in cur]
                return AnimeFull(*anime, episodes)
            else:
                return AnimeFull(*anime, None)

    def set_watched(self, aid, ep_type, number):
        """Set episode as watched."""
        self.cnx.cursor().execute(
            """UPDATE episode SET user_watched=:watched
            WHERE aid=:aid AND type=:type AND number=:number""",
            {
                'aid': aid,
                'type': ep_type,
                'number': number,
                'watched': 1,
            })

    def bump(self, aid):
        """Bump anime regular episode count."""
        anime = self.lookup(aid)
        if anime.complete:
            return
        episode = anime.watched_episodes + 1
        self.set_watched(aid, self.episode_types['regular'].id, episode)
        self.anime_cache.set_status(
            AnimeStatus(aid, episode >= anime.episodecount, episode))

    def cache_status(self, aid, force=False):
        """Calculate and cache status for given anime.

        Don't do anything if status already exists and force is False.

        """
        with self.cnx:
            cur = self.cnx.cursor()
            if not force:
                # We don't do anything if we already have this aid in our
                # cache.
                cur.execute(
                    'SELECT 1 FROM cache_anime WHERE aid=?',
                    (aid,))
                if cur.fetchone() is not None:
                    return

            # Retrieve number of episodes for this anime.
            cur.execute("""
                SELECT episodecount FROM anime WHERE aid=?
                """, (aid,))
            row = cur.fetchone()
            if row is None:
                raise ValueError('aid provided does not exist')
            episodecount = row[0]

            # Select all regular episodes in ascending order.
            cur.execute("""
                SELECT number, user_watched FROM episode
                WHERE aid=? AND type=?
                ORDER BY number ASC
                """, (aid, self.episode_types['regular'].id))

            # We find the last consecutive episode that is user_watched.
            number = 0
            for number, watched in cur:
                # Once we find the first unwatched episode, we set the last
                # consecutive watched episode to the previous episode (or 0).
                if watched == 0:
                    number -= 1
                    break
            # We store this in the cache.
            anime_status = AnimeStatus(aid, episodecount <= number, number)
            self.anime_cache.set_status(anime_status)

    def cache_files(self, aid, anime_files):
        with self.cnx:
            self.cache_status(aid)
            self.cnx.cursor().execute(
                """UPDATE cache_anime
                SET anime_files=?
                WHERE aid=?""",
                (aid, anime_files))

    def set_regexp(self, aid, regexp):
        """Set watching regexp for anime."""
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                'UPDATE watching SET regexp=? WHERE aid=?',
                (regexp, aid),
            )
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT INTO watching (aid, regexp)
                    VALUES (?, ?)""", (aid, regexp))

    def delete_regexp(self, aid):
        """Delete watching regexp for anime."""
        self.cnx.cursor().execute(
            """DELETE FROM watching WHERE aid=?""",
            (aid,))
