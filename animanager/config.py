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

import configparser
import os
import re
import shlex


class Config:

    DEF_PATH = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')
    DEF_VALUES = {
        'anime': {
            'database': '~/.animanager/database.db',
            'anidb_cache': '~/.animanager/anidb',
            'watchdir': '~/anime',
            'trashdir': '~/anime/trash',
            'player': 'mpv',
        },
    }
    _CONVERTERS = {
        'path': os.path.expanduser,
        'args': shlex.split,
    }

    def __init__(self, path=None):
        if path is None:
            path = self.DEF_PATH
        self.path = path
        self.config = configparser.ConfigParser(
            converters=self._CONVERTERS)
        self.config.read_dict(self.DEF_VALUES)
        self.config.read(self.path)

    def save(self):
        with open(self.path, 'w') as file:
            self.config.write(file)

    @property
    def anime(self):
        return self.Anime(self.config['anime'])

    class Anime:

        __slots__ = ['config']

        def __init__(self, config):
            self.config = config

        @property
        def database(self):
            """Anime database file."""
            return self.config.getpath('database')

        @property
        def anidb_cache(self):
            """AniDB cache directory."""
            return self.config.getpath('anidb_cache')

        @property
        def watchdir(self):
            """Directory to look for watching anime files."""
            return self.config.getpath('watchdir')

        @property
        def trashdir(self):
            """Directory to trash anime files."""
            return self.config.getpath('trashdir')

        @property
        def player(self):
            """Video player to use."""
            return self.config['player']
