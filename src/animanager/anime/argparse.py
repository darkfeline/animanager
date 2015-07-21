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

"""Argument parsing."""

from .bump import main as bump
from .add import main as add
from .update import main as update
from .stats import main as stats
from .watch import main as watch


def add_parsers(subparsers):

    """Add subparsers."""

    parser = subparsers.add_parser(
        'bump',
        description='Bump the episode count of a watched series.',
        help='Bump the episode count of a watched series.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.add_argument('--all', action='store_true',
                        help='Search all non-complete series.')
    parser.set_defaults(func=bump)

    parser = subparsers.add_parser(
        'add',
        description='Add a new series.',
        help='Add a new series.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.set_defaults(func=add)

    parser = subparsers.add_parser(
        'update',
        description='Update total episode count for series.',
        help='Update total episode count for series.',
    )
    parser.set_defaults(func=update)

    parser = subparsers.add_parser(
        'stats',
        description='Display statistics for shows.',
        help='Display statistics for shows.',
    )
    parser.set_defaults(func=stats)

    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=watch)
