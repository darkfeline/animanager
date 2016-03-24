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

from animanager.cmd.anime import AnimeCmd
from animanager.config import Config


def setup_parser(subparsers):

    """Setup parsers."""

    # Set up anime command parser.
    parser = subparsers.add_parser(
        'anime',
        description='Anime manager.',
        help='Start anime manager.',
    )
    parser.add_argument('script', nargs='?')
    parser.set_defaults(func=main)


def main(args):
    config = Config(args.config)
    if args.script:
        AnimeCmd.run_with_file(config, args.script)
    else:
        cmd = AnimeCmd(config)
        cmd.cmdloop()
