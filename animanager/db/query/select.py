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
from .status import STATUS_FIELDS, cache_status

logger = logging.getLogger(__name__)

SQLParams = Union[Sequence[Any], Mapping[str, Any]]

ANIME_FIELDS = {
    'aid': 'anime.aid',
    'title': 'title',
    'type': 'type',
    'episodecount': 'episodecount',
    'startdate': 'startdate',
    'enddate': 'enddate',
    'regexp': 'regexp',
}
ANIME_FIELDS.update(STATUS_FIELDS)

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
        unknown_fields = set(fields) - allowed_fields.keys()
        if unknown_fields:
            raise ValueError('Unknown fields: {}'.format(unknown_fields))
    return fields


ANIME_QUERY = """
    SELECT {}
    FROM anime
        LEFT JOIN cache_anime USING (aid)
        LEFT JOIN watching USING (aid)
    WHERE {}"""


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

    This will "lazily" fetch the requested fields as needed.  For example,
    episodes (which require a separate query per anime) will only be fetched if
    `episode_fields` is provided.  Anime status will be cached only if status
    fields are requested.

    :param str where_query: SELECT WHERE query
    :param where_params: parameters for WHERE query
    :param fields: anime fields to get.  If :const:`ALL`, get all fields.
        Default is :const:`ALL`.
    :param episode_fields: episode fields to get.
        If :const:`ALL`, get all fields.  If empty, don't get episodes.
        `fields` must contain 'aid' to get episodes.
    :param bool force_status: whether to force status calculation.
    :returns: iterator of Anime

    """

    logger.debug(
        'select(%r, %r, %r, %r, %r)',
        db, where_query, where_params, fields, episode_fields)
    fields = _clean_fields(ANIME_FIELDS, fields)
    if not fields:
        raise ValueError('Fields cannot be empty')
    if set(fields) & STATUS_FIELDS.keys():
        cur = db.cursor().execute(
            ANIME_QUERY.format('aid', where_query),
            where_params)
        for row in cur:
            cache_status(db, row[0])

    if 'aid' in fields:
        episode_fields = _clean_fields(EPISODE_FIELDS, episode_fields)
    else:
        episode_fields = ()

    with db:
        anime_query = ANIME_QUERY.format(
            ','.join(ANIME_FIELDS[field] for field in fields),
            where_query,
        )
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
        fields: FieldsParam = ALL,
        episode_fields: FieldsParam = (),
) -> Anime:
    """Look up information for a single anime.

    :param fields: anime fields to get.  If ``None``, get all fields.
    :param episode_fields: episode fields to get.
        If ``None``, get all fields.  If empty, don't get episodes.

    """
    return next(select(
        db,
        'aid=?',
        (aid,),
        fields=fields,
        episode_fields=episode_fields,
    ))
