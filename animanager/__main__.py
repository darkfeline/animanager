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

import argparse
import logging
import logging.config
import os

from animanager.animecmd import AnimeCmd
from animanager.config import Config
from animanager.config import load_config

_DEFAULT_CONFIG = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')


def main():
    """Animanager program entry point."""
    parser = _make_parser()
    args = parser.parse_args()
    _setup_logging(args)
    config = Config(args.config)
    config2 = load_config(args.config)
    cmd = AnimeCmd(config, config2)
    cmd.cmdloop()


def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default=_DEFAULT_CONFIG,
                        help='Alternate configuration file to use.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug output.')
    return parser


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


if __name__ == '__main__':
    main()
