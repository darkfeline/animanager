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

from animanager.cmds.anime import AnimeCmd
from animanager.config import Config

from .abc import Subcommand

__all__ = ['AnimeSubcommand']


class AnimeSubcommand(Subcommand):

    @classmethod
    def setup_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'anime',
            description='Anime manager.',
            help='Start anime manager.',
        )
        parser.set_defaults(func=cls.main)

    @staticmethod
    def main(args):
        config = Config(args.config)
        cmd = AnimeCmd(config)
        cmd.cmdloop()
