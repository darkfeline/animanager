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

from . import commands


def add_parsers(subparsers):

    parser = subparsers.add_parser('bump')
    parser.add_argument('name', nargs='?')
    parser.set_defaults(func=commands.bump)

    parser = subparsers.add_parser('add')
    parser.add_argument('name', nargs='?')
    parser.set_defaults(func=commands.add)

    parser = subparsers.add_parser('update')
    parser.set_defaults(func=commands.update)

    parser = subparsers.add_parser('stats')
    parser.set_defaults(func=commands.stats)
