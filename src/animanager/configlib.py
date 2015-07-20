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

"""Config loading stuff."""

import json
import os


class Config:

    def __init__(self, path=None):
        if path is None:
            path = self.defaultpath()
        self.path = path
        try:
            self.config = json.load(path)
        except OSError:
            raise ConfigError('Could not read config file {}'.format(path))

    @staticmethod
    def defaultpath():
        """Return default user config path."""
        return os.path.join(os.path.expanduser("~"), '.animanager.json')

    def save(self):
        with open(self.path, 'w') as file:
            json.dump(self.config, file)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value


class ConfigError(Exception):
    """Configuration error."""
