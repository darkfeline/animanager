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

import logging

from animanager import inputlib

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'hold',
        description='Put a series on hold.',
        help='Put a series on hold.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.add_argument('--all', action='store_true',
                        help='Search all non-complete series.')
    parser.set_defaults(func=main)


def _search(db, name, all=False):
    """Search for series."""
    if all:
        where_filter = 'status!="complete" AND name LIKE ?'
    else:
        where_filter = 'status="watching" AND name LIKE ?'
    results = db.select(
        table='anime',
        fields=['id', 'name'],
        where_filter=where_filter,
        where_args=('%{}%'.format(name),),
    )
    results = list(results)
    return results


def main(args):
    """Entry point."""
    choices = _search(args.db, args.name, args.all)
    i = inputlib.get_choice(['({}) {}'.format(x[0], x[1]) for x in choices])
    choice = choices[i]
    choice_id = choice[0]
    args.db.update_one('anime', choice_id, {'status': 'on hold'})
