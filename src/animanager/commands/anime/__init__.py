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

from .add import main as add
from .watch import main as watch

from . import stats
from . import update
from . import bump

_COMMANDS = [stats, update, bump]


def setup_parser(subparsers):

    """Setup parsers."""

    # Set up anime command parser.
    parser = subparsers.add_parser(
        'anime',
        description='Anime database manager.',
        help='Commands for interacting with anime database.',
    )
    subparsers = parser.add_subparsers(title='Commands')

    # Add anime subcommand parsers.

    parser = subparsers.add_parser(
        'add',
        description='Add a new series.',
        help='Add a new series.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.set_defaults(func=add)

    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=watch)

    for command in _COMMANDS:
        command.setup_parser(subparsers)
