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

from datetime import date
import logging

from animanager import inputlib
from animanager import mal

_LOGGER = logging.getLogger(__name__)
_STATUSES = ('plan to watch', 'watching', 'complete')


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'add',
        description='Add a new series.',
        help='Add a new series.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.set_defaults(func=main)


def main(args):

    # Get choices from MAL API.
    mal.query.setup(args.config)
    results = mal.query.anime_search(args.name)
    i = inputlib.get_choice(['({}) {}'.format(x.id, x.title) for x in results])

    # Set the fields for the row to add to the database.
    chosen = results[i]
    fields = {
        'animedb_id': chosen.id,
        'name': chosen.title,
        'type': chosen.type,
    }
    if chosen.episodes > 0:
        fields['ep_total'] = chosen.episodes

    # Choose initial status to set.
    i = inputlib.get_choice(_STATUSES, 0)
    fields['status'] = _STATUSES[i]
    if fields['status'] == 'complete':
        fields['ep_watched'] = fields['ep_total']
        today = date.today().isoformat()
        if inputlib.get_yn('Set start date to today?'):
            fields['date_started'] = today
        if inputlib.get_yn('Set finish date to today?'):
            fields['date_finished'] = today

    rowid = args.db.insert('anime', fields)

    if fields['status'] == 'watching':
        args.config.register(args.db, rowid)
        args.config.save()
