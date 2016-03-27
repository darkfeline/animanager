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

from typing import Any, Iterator


class StatusMixin:

    """Mixin for AnimeDB that implements status methods."""

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

            # Retrieve information for determining complete.
            cur.execute("""
                SELECT episodecount, enddate FROM anime WHERE aid=?
                """, (aid,))
            row = cur.fetchone()
            if row is None:
                raise ValueError('aid provided does not exist')
            episodecount, enddate = row

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
            self.set_status(aid, enddate and episodecount <= number, number)

    def set_status(
            self, aid: int, complete: Any, watched_episodes: int,
    ) -> None:
        """Set anime status."""
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                """UPDATE cache_anime
                SET complete=?, watched_episodes=?
                WHERE aid=?""",
                (complete,
                 watched_episodes,
                 aid))
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT INTO cache_anime
                    (aid, complete, watched_episodes)
                    VALUES (?, ?, ?)""",
                    (aid, 1 if complete else 0, watched_episodes))

    def get_complete(self) -> Iterator[int]:
        """Return AID of complete anime."""
        cur = self.cnx.cursor()
        cur.execute(
            """SELECT aid FROM cache_anime
            WHERE complete=?""", (1,))
        for row in cur:
            yield row[0]
