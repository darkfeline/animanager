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

import animanager
from animanager.animecmd import AnimeCmd
from animanager import config
from animanager import migrations

_DEFAULT_CONFIG = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')
_INTRO = f'''\
Animanager {animanager.__version__}
Copyright (C) 2015-2017  Allen Li

This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
This is free software, and you are welcome to redistribute it
under certain conditions; type "gpl c" for details.'''


def main():
    args = _parse_args()
    _setup_logging(args)
    cfg = config.load(args.config)
    db_path = cfg['anime'].getpath('database')
    migrations.migrate(str(db_path))
    cmd = AnimeCmd(cfg)
    print(_INTRO)
    cmd.cmdloop()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        default=_DEFAULT_CONFIG,
                        help='Alternate configuration file to use.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug output.')
    return parser.parse_args()


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
