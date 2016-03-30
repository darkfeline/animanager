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

from animanager.date import timestamp

logger = logging.getLogger(__name__)


class UpdateMixin:

    """Update commands (write) for AnimeDB."""

    def add(self, anime):
        """Add an anime (or update existing).

        anime is an AnimeTree instance.

        """
        values = {
            'aid': anime.aid,
            'title': anime.title,
            'type': anime.type,
            'episodecount': anime.episodecount,
            'startdate': anime.startdate,
            'enddate': anime.enddate,
        }
        if anime.startdate is not None:
            values['startdate'] = timestamp(anime.startdate)
        if anime.enddate is not None:
            values['enddate'] = timestamp(anime.enddate)
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """UPDATE anime
                SET title=:title, type=:type, episodecount=:episodecount,
                    startdate=:startdate, enddate=:enddate
                WHERE aid=:aid""", values)
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT INTO anime (
                        aid, title, type, episodecount,
                        startdate, enddate)
                    VALUES (
                        :aid, :title, :type, :episodecount,
                        :startdate, :enddate)""", values)
            for episode in anime.episodes:
                self.add_episode(anime.aid, episode)

    def add_episode(self, aid, episode):
        with self.cnx:
            cur = self.cnx.cursor()
            values = {
                'aid': aid,
                'type': episode.type,
                'number': episode.number,
                'title': episode.title,
                'length': episode.length,
            }
            cur.execute(
                """UPDATE episode
                SET title=:title, length=:length
                WHERE aid=:aid AND type=:type AND number=:number""",
                values)
            if self.cnx.changes() == 0:
                values['user_watched'] = 0
                cur.execute(
                    """INSERT INTO episode (
                        aid, type, number, title,
                        length, user_watched)
                    VALUES (
                        :aid, :type, :number, :title,
                        :length, :user_watched)""", values)

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
        with self.cnx:
            self.set_watched(aid, self.episode_types['regular'].id, episode)
            self.set_status(
                aid, anime.enddate and episode >= anime.episodecount, episode)

    def reset(self, aid, episode):
        """Reset episode count for anime."""
        params = {
            'aid': aid,
            'type': self.episode_types['regular'],
            'watched': 1,
            'number': episode,
        }
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """UPDATE episode SET user_watched=:watched
                WHERE aid=:aid AND type=:type AND number<=:number""",
                params)
            params['watched'] = 0
            cur.execute(
                """UPDATE episode SET user_watched=:watched
                WHERE aid=:aid AND type=:type AND number>:number""",
                params)
            self.cache_status(aid, force=True)
