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

"""Implements add command."""

from collections import OrderedDict
from datetime import date
import logging
from urllib.parse import urlencode

from animanager import inputlib
from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

_LOGGER = logging.getLogger(__name__)
_MAL_SEARCH = "http://myanimelist.net/api/anime/search.xml?"
_STATUSES = ('plan to watch', 'watching', 'complete')


def _get_datum(entity, key):
    """Get the XML entity's value for the given key."""
    return entity.find(key).text

_DATA_KEYS = ('id', 'title', 'episodes', 'type')

def _get_data(entity):
    """Get entry data from XML tree."""
    return [_get_datum(entity, key) for key in _DATA_KEYS]


def main(args):

    """Add command."""

    config = args.config
    name = args.name

    # Get choices from MAL API
    response = ffrequest(_MAL_SEARCH + urlencode({'q': name}))
    response = response.read().decode()
    tree = xmllib.parse(response)
    found = [_get_data(entity) for entity in list(tree)]
    i = inputlib.get_choice(['{} {}'.format(x[0], x[1]) for x in found])

    # Set data fields
    args = OrderedDict(zip(['animedb_id', 'name', 'ep_total', 'type'],
                           found[i]))

    i = inputlib.get_choice(_STATUSES, 0)
    args['status'] = _STATUSES[i]

    if args['status'] == 'watching':
        confirm = input('Set start date to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
    elif args['status'] == 'complete':
        args['ep_watched'] = args['ep_total']
        confirm = input('Set dates to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            today = date.today().isoformat()
            args['date_started'] = today
            args['date_finished'] = today

    query = 'INSERT INTO anime SET {}'.format(
        ', '.join('{}=%s'.format(key) for key in args))
    values = list(args.values())
    _LOGGER.debug('query %r %r', query, values)
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(query, values)
