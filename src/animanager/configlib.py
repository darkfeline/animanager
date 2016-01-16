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

"""This module contains stuff related to configuration."""

import configparser
import os
import re
import shlex
from collections import defaultdict


class Config:

    """Config class.

    This class handles configuration loading, saving, checking, and
    manipulation.

    """

    DEF_PATH = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')
    DEF_VALUES = {
        'general': {
            'database': '~/.animanager/database.db',
        },
        'watch': {
            'player': 'mpv',
        },
        'series': {},
        'mal_args': {},
    }
    REQ_VALUES = {
        'general': ['database'],
        'watch': ['player', 'directory'],
        'series': [],
        'mal_args': ['user', 'passwd'],
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
        self._check()

    def _check(self):
        """Check that all required configuration keys have been provided.

        Raises MissingConfigKeysError.

        """
        missing = defaultdict(list)
        for section in self.REQ_VALUES:
            for key in self.REQ_VALUES[section]:
                if key not in self.config[section]:
                    missing[section].append(key)
        if missing:
            raise MissingConfigKeysError(missing)

    def save(self):
        with open(self.path, 'w') as file:
            self.config.write(file)

    def __getitem__(self, key):
        return self.config[key]

    def register(self, db, id):
        results = db.select(
            table='anime',
            fields=['name'],
            where_filter='id=?',
            where_args=(id,)
        )
        name = next(results)[0]
        # Replace non-word, non-whitespace with whitespace.
        pattern = re.sub(r'[^\w\s]', ' ', name)
        # Split on whitespace and join with wildcard regexp.
        pattern = '.*'.join(re.escape(x) for x in pattern.split())
        # Append episode matching pattern.
        pattern = '.*?'.join((
            pattern,
            r'\b(?P<ep>[0-9]+)(v[0-9]+)?',
        ))
        self['series'][str(id)] = pattern

    def unregister(self, id):
        del self['series'][str(id)]


class ConfigError(Exception):
    pass


class MissingConfigKeysError(ConfigError):

    def __init__(self, missing):
        self.missing = missing

    def __str__(self):
        return "Missing configuration values: {}".format(
            '; '.join(
                'in [{}], {}'.format(section, ', '.join(self.missing[section]))
                for section in self.missing))
