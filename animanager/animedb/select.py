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
from typing import Any, Iterator, Mapping, Sequence, Union

from .collections import Anime, AnimeFull, Episode

logger = logging.getLogger(__name__)


class SelectMixin:

    """Select commands (read only) for AnimeDB."""

    def select(
            self, where_query: str,
            params: Union[Sequence[Any], Mapping[str, Any]],
    ) -> Iterator[Anime]:
        """Perform an arbitrary SQL SELECT WHERE on the anime table.

        Returns an Anime instance generator.  Caches anime status lazily.

        """
        aids = self.cnx.cursor()
        aids.execute(
            """SELECT aid FROM anime
            LEFT JOIN watching USING (aid)
            WHERE {}
            ORDER BY aid ASC
            """.format(where_query),
            params)
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
            row = cur.fetchone()
            if row is not None:
                yield Anime(*row)

    def lookup_title(self, aid):
        """Look up anime title."""
        cur = self.cnx.cursor()
        cur.execute('SELECT title FROM anime WHERE aid=?', (aid,))
        anime = cur.fetchone()
        if anime is None:
            raise ValueError('Invalid aid')
        return anime[0]

    def lookup(self, aid, include_episodes=False):
        """Look up full information for a single anime.

        If episodes is True, individual episodes will be looked up and included
        in the returned AnimeFull instance.  Otherwise, the episodes attribute
        on the returned AnimeFull instance will be an empty list.

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
            if include_episodes:
                cur.execute("""
                    SELECT aid, type, number, title, length, user_watched
                    FROM episode WHERE aid=?""", (aid,))
                episodes = [Episode(*row) for row in cur]
            else:
                episodes = []
            return AnimeFull(*anime, episodes)
