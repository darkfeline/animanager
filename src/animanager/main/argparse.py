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

import argparse

from animanager import configlib
from animanager.anime import argparse as anime


def make_parser():

    """Make an ArgumentParser."""

    # Set up main parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=configlib.load_config,
                        default=configlib.default_config())
    parser.add_argument('--debug', action='store_true')

    # Set up subparsers
    subparsers = parser.add_subparsers(title='Managers')

    # Set up anime subsubparser
    subparser = subparsers.add_parser('anime')
    subsubparsers = subparser.add_subparsers(title='Commands')
    anime.add_parsers(subsubparsers)

    return parser