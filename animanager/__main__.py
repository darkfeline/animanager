# Copyright (C) 2015-2016  Allen Li
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

import argparse
import logging

from animanager import subcommands


def _make_parser():
    # Set up main parser.
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default='',
                        help='Alternate configuration file to use.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug output.')

    # Set up subparsers.
    subparsers = parser.add_subparsers(title='Managers')
    subcommands.AnimeSubcommand.setup_parser(subparsers)

    return parser


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(levelname)s:%(name)s:%(message)s',
    ))
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    parser = _make_parser()
    args = parser.parse_args()

    if not args.debug:
        handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s',
        ))
        root_logger.setLevel(logging.INFO)

    # Run command.
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)

if __name__ == '__main__':
    main()
