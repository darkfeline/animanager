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

from animanager.dblib import FIELDS


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'watching',
        description='Show watching series data.',
        help='Show watching series data.',
    )
    parser.set_defaults(func=main)


def main(args):
    shows = args.db.select(
        'anime',
        FIELDS,
        'status="watching"'
    )
    print(tabulate(shows, headers=FIELDS))
