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

import sys
import logging

from animanager import mal
from animanager import inputlib

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'update',
        description='Update total episode count for series.',
        help='Update total episode count for series.',
    )
    parser.set_defaults(func=main)


def _anime_iter(db):
    """Return a generator of anime database entries."""
    return db.select(
        table='anime',
        fields=['id', 'animedb_id', 'name', 'ep_total'],
        where_filter='ep_total IS NULL OR status = "watching"',
    )


def main(args):
    """Update command."""

    db = args.db
    config = args.config
    mal.query.setup(config)

    # Keep lists of things to update.
    # Tuples of ids and total episode counts to update.
    to_update = []
    # Tuples of ids and series names to update.
    to_rename = []
    for id, mal_id, name, eps in _anime_iter(db):
        _LOGGER.debug("Our entry id=%r, name=%r, eps=%r", id, name, eps)

        # Search for our show on MAL, and make sure to match our MAL id.
        try:
            results = mal.query.anime_search(name)
        except mal.ResponseError:
            _LOGGER.warning('No results found for id=%r, name=%r', id, name)
            continue
        results = dict((result.id, result) for result in results)
        found = results[mal_id]
        found_title, found_eps = found.title, found.episodes
        _LOGGER.debug('Found mal_id=%r, name=%r, eps=%r',
                      mal_id, found_title, found_eps)

        # If their name is different from our name, prompt for action.
        if found_title != name:
            print('Found {}, our name is {}'.format(found_title, name))
            choice = inputlib.get_choice(["Use MAL's name",
                                          "Ignore",
                                          "Abort"], 0)
            if choice == 0:
                to_rename.append((id, found_title))
            elif choice == 2:
                _LOGGER.info('Aborting...')
                sys.exit(1)
        if found_eps != 0:
            assert found_eps > 0
            to_update.append((id, found_eps))
    if to_rename:
        _LOGGER.info('Renaming local entries...')
        db.update_many('anime', ['name'], to_rename)
    if to_update:
        _LOGGER.info('Updating local entries...')
        db.update_many('anime', ['ep_total'], to_update)


class Error(Exception):
    """General error."""
