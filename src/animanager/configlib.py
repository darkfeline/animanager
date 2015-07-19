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


def load_config(path=None):
    """Load config from file."""
    if path is None:
        path = default_config()
    with open(path) as file:
        config = json.load(file)
    return config


def save_config(config, path=None):
    if path is None:
        path = default_config()
    with open(path, 'w') as file:
        json.dump(config, file)


def default_config():
    """Return default user config path."""
    return os.path.join(os.path.expanduser("~"), '.anime.cfg')
