# Copyright (C) 2015  Allen Li
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

"""Update command."""

import logging

from animanager import dblib
from animanager import mal

_LOGGER = logging.getLogger(__name__)


def anime_iter(dbconfig):
    """Return a generator of anime database entries."""
    return dblib.select(dbconfig,
                        'anime',
                        ['id', 'animedb_id', 'name', 'ep_total'],
                        'ep_total = 0 OR status = "watching"',)


def main(args):
    """Update command."""
    config = args.config
    mal.setup(config)
    to_update = []
    for my_id, mal_id, name, my_eps in anime_iter(config['db_args']):
        # Search for our show on MAL, and make sure to match our MAL id.
        _LOGGER.debug("Our entry id=%r, name=%r, eps=%r", my_id, name, my_eps)
        try:
            results = mal.anime_search(name)
        except mal.ResponseError:
            _LOGGER.warning('No results found for id=%r, name=%r', my_id, name)
            continue
        results = dict((result.id, result) for result in results)
        found = results[mal_id]
        found_title, found_eps = found.title, found.episodes
        _LOGGER.debug('Found mal_id=%r, name=%r, eps=%r',
                      mal_id, found_title, found_eps)
        if found_title != name:
            raise Error('Found {}, our name is {}'.format(
                found_title, name))
        if found_eps != 0:
            assert found_eps > 0
            to_update.append((my_id, found_eps))
    _LOGGER.info('Updating local entries')
    dblib.update_many(config['db_args'], 'anime', ['ep_total'], to_update)


class Error(Exception):
    """General error."""
