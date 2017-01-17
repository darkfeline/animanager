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

__all__ = ['Config']


class _ConfigMeta(type):

    """Metaclass for defining config classes.

    Config classes should define a nested class Sections, which should
    define nested classes (section classes) for INI section access.
    Each section class should define methods for accessing INI
    configuration options in that section.

    A property will be created for each section class, which will return
    an object that will further have properties corresponding to that
    section class's methods.

    You should probably just look at how it's being used.
    """

    def __new__(mcs, name, parents, dct):
        sections = dct['Sections']
        for name, section_cls in sections.__dict__.items():
            if name.startswith('_'):
                continue
            mcs._add_section(dct, name, section_cls)
        return super().__new__(mcs, name, parents, dct)

    @staticmethod
    def _add_section(dct, name, section_cls):
        dispatcher_class = _make_section_dispatcher(
            name=name,
            dct={
                name: property(getter)
                for name, getter in section_cls.__dict__.items()
            })
        dct[name] = property(lambda self: dispatcher_class(self._config))


def _make_section_dispatcher(name, dct):
    """Make session dispatcher."""
    dct['__slots__'] = ('_config',)
    def __init__(self, config):
        self._config = config[name]
    dct['__init__'] = __init__
    return type(name, (), dct)


class _BaseConfig(metaclass=_ConfigMeta):

    _DEF_VALUES = {}
    _CONVERTERS = {}

    def __init__(self, path: 'PathLike'):
        self._path = Path(path)
        self._config = configparser.ConfigParser(
            converters=self._CONVERTERS)

        self._config.read_dict(self._DEF_VALUES)
        with self._path.open() as file:
            self._config.read_file(file)

    def save(self):
        with self._path.open('w') as file:
            self._config.write(file)

    class Sections:
        pass


class Config(_BaseConfig):

    _DEF_PATH = Path.home() / '.animanager' / 'config.ini'
    _DEF_VALUES = {
        'general': {
            'backup_before_migration': 'true',
            'colors': 'false',
        },
        'anime': {
            'database': '~/.animanager/database.db',
            'anidb_cache': '~/.animanager/anidb',
            'watchdir': '~/anime',
            'player': 'mpv',
        },
    }
    _CONVERTERS = {
        'path': lambda x: Path(x).expanduser(),
        'args': shlex.split,
    }

    def __init__(self, path: 'PathLike' = ''):
        if path:
            path = Path(path)
        else:
            path = self._DEF_PATH
        super().__init__(path)

    class Sections:

        class general:

            def colors(self):
                """Enable colors."""
                return self._config.getboolean('colors')

            def backup_before_migration(self):
                """Video player to use."""
                return self._config.getboolean('backup_before_migration')

        class anime:

            def database(self):
                """Anime database file."""
                return self._config.getpath('database')

            def anidb_cache(self):
                """AniDB cache directory."""
                return self._config.getpath('anidb_cache')

            def watchdir(self):
                """Directory to look for watching anime files."""
                return self._config.getpath('watchdir')

            def player_args(self):
                """Video player to use."""
                return self._config.getargs('player')
