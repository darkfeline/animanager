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
from urllib.parse import urlencode

from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

_LOGGER = logging.getLogger(__name__)

_MAL_SEARCH = "http://myanimelist.net/api/anime/search.xml?"


def _get_datum(entity, key):
    """Get the XML entity's value for the given key."""
    return entity.find(key).text

_DATA_KEYS = ('id', 'title', 'episodes')

def _get_data(entity):
    """Get entry data from XML tree."""
    return [_get_datum(entity, key) for key in _DATA_KEYS]


def anime_iter(config):
    """Return a generator of anime database entries."""
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(' '.join((
            'SELECT id, animedb_id, name, ep_total FROM anime',
            'WHERE ep_total = 0',
            'OR status = "watching"',
        )))
        while True:
            row = cur.fetchone()
            if row:
                yield row
            else:
                break


def update_entries(config, to_update):
    """Update anime database entries."""
    with mysqllib.connect(**config["db_args"]) as cur:
        print('Setting episode totals')
        cur.executemany('UPDATE anime SET ep_total=%s WHERE id=%s', to_update)
        print('Setting complete as needed')
        cur.execute(' '.join((
            'UPDATE anime SET status="complete"',
            'WHERE ep_total = ep_watched AND ep_total != 0',
        )))


def main(args):
    """Update command."""
    config = args.config
    to_update = []
    for my_id, mal_id, name, my_eps in anime_iter(config):
        # Search for our show on MAL, and make sure to match our MAL id.
        _LOGGER.debug("Our entry id=%r, name=%r, eps=%r", my_id, name, my_eps)
        response = ffrequest(_MAL_SEARCH + urlencode({'q': name}))
        response = response.read().decode()
        _LOGGER.debug(response)
        tree = xmllib.parse(response)
        if tree is None:
            _LOGGER.warning('No results found for id=%r, name=%r', my_id, name)
            continue
        found = [_get_data(entity) for entity in list(tree)]
        found = dict((int(entry[0]), entry[1:]) for entry in found)
        found_title, found_eps = found[mal_id]
        found_eps = int(found_eps)
        _LOGGER.debug('Found mal_id=%r, name=%r, eps=%r',
                      mal_id, found_title, found_eps)
        if found_title != name:
            raise Error('Found {}, our name is {}'.format(
                found_title, name))
        if found_eps != 0:
            assert found_eps > 0
            to_update.append((found_eps, my_id))
    _LOGGER.info('Updating local entries')
    update_entries(config, to_update)


class Error(Exception):
    """General error."""
