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

from animanager import inputlib


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'register',
        description='Register a watching series in config.',
        help='Register a watching series in config.',
    )
    parser.add_argument('name')
    parser.set_defaults(func=main)


def main(args):
    results = args.db.select(
        'anime',
        ['id', 'name'],
        'status="watching" AND name LIKE ?',
        ('%{}%'.format(args.name),)
    )
    results = list(results)
    i = inputlib.get_choice(['({}) {}'.format(x[0], x[1]) for x in results])
    args.config.register(args.db, results[i][0])
    args.config.save()
