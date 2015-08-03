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

"""Stats command."""

from animanager import dblib


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'stats',
        description='Display statistics for shows.',
        help='Display statistics for shows.',
    )
    parser.set_defaults(func=main)


def main(args):
    """Stats command."""
    with dblib.Database().connect() as cur:
        print('By status:')
        cur.execute('SELECT id, name FROM anime_statuses')
        for id, name in cur.fetchall():
            cur.execute('SELECT count(*) FROM anime WHERE status=?', [id])
            print('- {}: {}'.format(name, cur.fetchone()[0]))

        cur.execute('SELECT count(*) FROM anime')
        print('Total: {}'.format(cur.fetchone()[0]))

        cur.execute('SELECT SUM(ep_watched) FROM anime')
        print('Episodes watched: {}'.format(cur.fetchone()[0]))
