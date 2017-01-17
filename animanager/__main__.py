# Copyright (C) 2015-2017  Allen Li
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

import abc
import argparse
import logging
import logging.config

from animanager.animecmd import AnimeCmd
from animanager.config import Config


def main():
    """Animanager program entry point."""
    parser = _make_parser()
    args = parser.parse_args()
    _setup_logging(args)
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)


def _make_parser():
    parser = _make_root_parser()
    _add_command_parsers(parser)
    return parser


def _make_root_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default='',
                        help='Alternate configuration file to use.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug output.')
    return parser


def _add_command_parsers(parser):
    subparsers = parser.add_subparsers(title='Commands')
    for command in _commands:
        command.setup_parser(subparsers)


def _setup_logging(args):
    logging.config.dictConfig({
        'version': 1,
        'root': {
            'level': 'DEBUG' if args.debug else 'INFO',
            'handlers': ['console'],
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s: %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s:%(name)s:%(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose' if args.debug else 'simple',
            },
        },
        'disable_existing_loggers': False,
    })


_commands = []


def _add_command(command):
    """Decorator for adding command classes."""
    _commands.append(command())
    return command


class _Command(metaclass=abc.ABCMeta):

    """ABC for a main script command."""

    @abc.abstractmethod
    def setup_parser(self, subparsers):
        """Add subparser for command."""

    @abc.abstractmethod
    def main(self, args):
        """Subroutine for command."""


@_add_command
class _AnimeCommand(_Command):

    def setup_parser(self, subparsers):
        parser = subparsers.add_parser(
            'anime',
            description='Anime manager.',
            help='Start anime manager.',
        )
        parser.set_defaults(func=self.main)

    def main(self, args):
        config = Config(args.config)
        cmd = AnimeCmd(config)
        cmd.cmdloop()


if __name__ == '__main__':
    main()
