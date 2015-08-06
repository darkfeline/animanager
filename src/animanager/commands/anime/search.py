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

from tabulate import tabulate


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'search',
        description='Search for series data.',
        help='Search for series data.',
    )
    parser.add_argument('name')
    parser.set_defaults(func=main)

_FIELDS = ['id', 'name', 'type', 'ep_watched', 'ep_total', 'status',
           'date_started', 'date_finished', 'animedb_id']


def main(args):
    shows = args.db.select(
        'anime',
        _FIELDS,
        'name LIKE ?',
        ['%{}%'.format(args.name)]
    )
    print(tabulate(shows, headers=_FIELDS))
