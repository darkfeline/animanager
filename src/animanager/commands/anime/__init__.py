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

from . import stats
from . import update
from . import bump
from . import add
from . import search
from . import watch
from . import clean
from . import register

_COMMANDS = [stats, update, bump, add, search, watch, clean, register]


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
    for command in _COMMANDS:
        command.setup_parser(subparsers)
