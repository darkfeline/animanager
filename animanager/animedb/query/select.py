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
from typing import Any, Iterable, Iterator, Mapping, Sequence, Union

from .collections import Anime, Episode
from .status import cache_status

logger = logging.getLogger(__name__)

SQLParams = Union[Sequence[Any], Mapping[str, Any]]

ANIME_FIELDS = {
    'aid': 'anime.aid',
    'title': 'title',
    'type': 'type',
    'episodecount': 'episodecount',
    'startdate': 'startdate',
    'enddate': 'enddate',
    'complete': 'complete',
    'regexp': 'regexp',
}

EPISODE_FIELDS = {
    'aid': 'aid',
    'type': 'type',
    'number': 'number',
    'title': 'title',
    'length': 'length',
    'user_watched': 'user_watched',
}

ALL = 1
"""Flag for selecting all fields."""

FieldsParam = Union[Iterable[str], int]


def _clean_fields(allowed_fields: dict, fields: FieldsParam) -> Iterable[str]:
    """Clean lookup fields and check for errors."""
    if fields == ALL:
        fields = allowed_fields.keys()
    else:
        fields = tuple(fields)
        unknown_fields = set(fields) & allowed_fields.keys()
        if unknown_fields:
            raise ValueError('Unknown fields: {}'.format(unknown_fields))
    return fields


def select(
        db,
        where_query: str,
        where_params: SQLParams,
        fields: FieldsParam = ALL,
        episode_fields: FieldsParam = (),
) -> Iterator[Anime]:
    """Perform an arbitrary SQL SELECT WHERE on the anime table.

    By nature of "arbitrary query", this is vulnerable to injection, use only
    trusted values for `where_query`.

    :param str where_query: SELECT WHERE query
    :param where_params: parameters for WHERE query
    :param fields: anime fields to get.  If :const:`ALL`, get all fields.
        Default is :const:`ALL`.
    :param episode_fields: episode fields to get.
        If :const:`ALL`, get all fields.  If empty, don't get episodes.
        `fields` must contain 'aid' to get episodes.
    :returns: iterator of Anime

    """

    fields = _clean_fields(ANIME_FIELDS, fields)
    if not fields:
        raise ValueError('Fields cannot be empty')
    if 'aid' in fields:
        episode_fields = _clean_fields(ANIME_FIELDS, episode_fields)
    else:
        episode_fields = ()

    with db:
        anime_query = """
            SELECT {}
            FROM anime
                JOIN cache_anime USING (aid)
                LEFT JOIN watching USING (aid)
            WHERE {}""".format(where_query)
        anime_query = anime_query.format(
            ','.join(ANIME_FIELDS[field] for field in fields))

        anime_rows = db.cursor().execute(anime_query, where_params)
        for row in anime_rows:
            anime = Anime(**{
                field: value
                for field, value in zip(fields, row)})

            if episode_fields:
                episode_query = 'SELECT {} FROM episode WHERE aid=?'
                episode_query = episode_query.format(
                    ','.join(EPISODE_FIELDS[field] for field in episode_fields))

                episode_rows = db.cursor().execute(episode_query, (anime.aid,))
                episodes = [
                    Episode(**{
                        field: value
                        for field, value in zip(episode_fields, row)})
                    for row in episode_rows]
                anime.episodes = episodes

            yield anime


def lookup(
        db,
        aid: int,
) -> Anime:
    """Look up full information for a single anime.

    This forces status calculation.

    :param fields: anime fields to get.  If ``None``, get all fields.
    :param episode_fields: episode fields to get.
        If ``None``, get all fields.  If empty, don't get episodes.

    """
    cache_status(db, aid)
    return next(select(
        db,
        'aid=?',
        (aid,),
        fields=ALL,
        episode_fields=ALL,
    ))
