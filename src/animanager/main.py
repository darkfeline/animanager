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
import argparse

from animanager import configlib
from animanager import dblib

from animanager.commands import anime


def _make_parser():

    """Make the root argument parser for the animanager program."""

    # Set up main parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default=configlib.Config.defaultpath,
                        help='Alternate configuration file to use.')
    parser.add_argument('--db',
                        default=dblib.Database.defaultpath,
                        help='Alternate database file to use.')

    # Set up subparsers
    subparsers = parser.add_subparsers(title='Managers')
    anime.setup_parser(subparsers)

    return parser


def main():
    """Entry function."""
    logging.basicConfig(level='INFO')
    parser = _make_parser()
    args = parser.parse_args()

    args.config = configlib.Config(args.config)
    args.db = dblib.Database(args.db)

    # Run command.
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)

if __name__ == '__main__':
    main()
