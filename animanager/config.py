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

import configparser
from pathlib import Path
import shlex

_CONVERTERS = {
    'path': lambda x: Path(x).expanduser(),
    'args': shlex.split,
}
_DEFAULTS = {
    'general': {
        'colors': 'false',
    },
    'anime': {
        'database': '~/.animanager/database.db',
        'anidb_cache': '~/.animanager/anidb',
        'watchdir': '~/anime',
        'player': 'mpv',
    },
}


def load_config(path):
    parser = configparser.ConfigParser(
        converters=_CONVERTERS)
    parser.read_dict(_DEFAULTS)
    with open(path) as f:
        parser.read_file(f)
    return parser
