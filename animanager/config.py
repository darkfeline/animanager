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
import shlex
from typing import Any, Callable, Dict


# pylint: disable=too-few-public-methods


def _make_section(dct, section_name, section_dct):
    """Make session dispatcher."""
    # __slots__
    section_dct['__slots__'] = ('config',)
    # __init__
    def __init__(self, config):
        self.config = config[section_name]
    section_dct['__init__'] = __init__
    # Making the class.
    section_class = type(section_name, (), section_dct)
    # Making the property.
    dct[section_name] = property(lambda self: section_class(self.config))


class ConfigMeta(type):

    """Metaclass for defining config classes.

    Config classes should define a nested class Sections, which should define
    nested classes (section classes) for INI section access.  Each section
    class should define methods for accessing INI configuration options in that
    section.

    A property will be created for each section class, which will return an
    object that will further have properties corresponding to that section
    class's methods.

    You should probably just look at how it's being used.

    """

    def __new__(mcs, name, parents, dct):
        sections = dct['Sections']
        for section_name, section in sections.__dict__.items():
            if section_name.startswith('_'):
                continue
            section_dct = dict()
            for config_name, config_getter in section.__dict__.items():
                section_dct[config_name] = property(config_getter)
            _make_section(dct, section_name, section_dct)
        return super().__new__(mcs, name, parents, dct)


class BaseConfig(metaclass=ConfigMeta):

    DEF_VALUES = {}  # type: Dict[str, Dict[str, Any]]
    CONVERTERS = {}  # type: Dict[str, Callable[[str], Any]]

    def __init__(self, path: str) -> None:
        self.path = path
        self.config = configparser.ConfigParser(
            converters=self.CONVERTERS)
        self.config.read_dict(self.DEF_VALUES)
        self.config.read(self.path)

    def save(self):
        with open(self.path, 'w') as file:
            self.config.write(file)

    class Sections:
        pass


class Config(BaseConfig):

    DEF_PATH = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')
    DEF_VALUES = {
        'general': {
            'backup_before_migration': 'true',
        },
        'anime': {
            'database': '~/.animanager/database.db',
            'anidb_cache': '~/.animanager/anidb',
            'watchdir': '~/anime',
            'player': 'mpv',
        },
    }
    CONVERTERS = {
        'path': os.path.expanduser,
        'args': shlex.split,
    }

    def __init__(self, path: str = '') -> None:
        if not path:
            path = self.DEF_PATH
        super().__init__(path)

    class Sections:

        # pylint: disable=no-member

        class general:

            def backup_before_migration(self):
                """Video player to use."""
                return self.config.getboolean('backup_before_migration')

        class anime:

            def database(self):
                """Anime database file."""
                return self.config.getpath('database')

            def anidb_cache(self):
                """AniDB cache directory."""
                return self.config.getpath('anidb_cache')

            def watchdir(self):
                """Directory to look for watching anime files."""
                return self.config.getpath('watchdir')

            def player_args(self):
                """Video player to use."""
                return self.config.getargs('player')
