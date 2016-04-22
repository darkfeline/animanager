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

"""Select type queries."""

import logging
from typing import Any, Iterable, Iterator, Mapping, Optional, Sequence, Union

from .collections import Anime, Episode
from .status import cache_status

logger = logging.getLogger(__name__)

SQLParams = Union[Sequence[Any], Mapping[str, Any]]


def select(db, where_query: str, params: SQLParams,) -> Iterator[int]:
    """Perform an arbitrary SQL SELECT WHERE on the anime table.

    By nature of "arbitrary query", this is vulnerable to injection, use only
    trusted values for `where_query`.

    :returns: an iterator of AIDs

    """
    aids = db.cursor()
    aids.execute(
        """SELECT aid FROM anime
        LEFT JOIN watching USING (aid)
        WHERE {}
        ORDER BY aid ASC
        """.format(where_query),
        params)
    for aid in aids:
        yield aid

LOOKUP_ANIME_FIELDS = {
    'aid': 'anime.aid',
    'title': 'title',
    'type': 'type',
    'episodecount': 'episodecount',
    'startdate': 'startdate',
    'enddate': 'enddate',
    'complete': 'complete',
    'regexp': 'regexp',
}

LOOKUP_EPISODE_FIELDS = {
    'aid': 'aid',
    'type': 'type',
    'number': 'number',
    'title': 'title',
    'length': 'length',
    'user_watched': 'user_watched',
}


def _clean_fields(allowed_fields: dict, fields: Optional[Iterable]):
    """Clean lookup fields and check for errors."""
    if fields is None:
        fields = allowed_fields.keys()
    fields = tuple(fields)
    unknown_fields = set(fields) & allowed_fields.keys()
    if unknown_fields:
        raise ValueError('Unknown fields: {}'.format(unknown_fields))
    return fields


def lookup(
        db,
        aid: int,
        fields: Optional[Iterable] = None,
        episode_fields: Optional[Iterable] = (),
) -> Anime:
    """Look up full information for a single anime.

    This forces status calculation.

    :param fields: anime fields to get.  If ``None``, get all fields.
    :param episode_fields: episode fields to get.
        If ``None``, get all fields.  If empty, don't get episodes.

    """

    fields = _clean_fields(LOOKUP_ANIME_FIELDS, fields)
    if not fields:
        raise ValueError('Fields cannot be empty')
    episode_fields = _clean_fields(LOOKUP_ANIME_FIELDS, episode_fields)

    cache_status(db, aid, force=True)
    with db:
        cur = db.cursor()
        anime_query = """
            SELECT {}
            FROM anime
                JOIN cache_anime USING (aid)
                LEFT JOIN watching USING (aid)
            WHERE anime.aid=?"""
        anime_query = anime_query.format(
            ','.join(LOOKUP_ANIME_FIELDS[field] for field in fields))

        cur.execute(anime_query, (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('Invalid aid')
        anime = Anime(**{
            field: value
            for field, value in zip(fields, row)})

        if episode_fields:
            episode_query = 'SELECT {} FROM episode WHERE aid=?'
            episode_query = episode_query.format(
                ','.join(
                    LOOKUP_EPISODE_FIELDS[field]
                    for field in episode_fields))

            cur.execute(episode_query, (aid,))
            episodes = [
                Episode(**{
                    field: value
                    for field, value in zip(episode_fields, row)})
                for row in cur]
            anime.episodes = episodes

        return anime
