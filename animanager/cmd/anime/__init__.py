# Copyright (C) 2016  Allen Li
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

import logging
# readline is needed for command editing.
import readline  # pylint: disable=unused-import
import traceback
from cmd import Cmd
from textwrap import dedent

from animanager import __version__ as VERSION
from animanager.anidb import AniDB, SearchDB
from animanager.animedb import AnimeDB
from animanager.argparse import CommandError
from animanager.cache import BaseCacheHolder, cached_property
from animanager.files import FilePicker, PriorityRule
from animanager.results.aid import AIDResults, AIDResultsManager

from . import anidb, animedb, gpl, misc, watching

logger = logging.getLogger(__name__)


class AnimeCmd(Cmd, BaseCacheHolder):

    # pylint: disable=no-self-use,unused-argument,too-many-instance-attributes

    intro = dedent('''\
    Animanager {}
    Copyright (C) 2015-2016  Allen Li

    This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
    This is free software, and you are welcome to redistribute it
    under certain conditions; type "gpl c" for details.''').format(VERSION)
    prompt = 'A> '

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

        self.anidb = AniDB(config.anime.anidb_cache)
        self.searchdb = SearchDB(config.anime.anidb_cache)
        self.animedb = AnimeDB(config.anime.database)

        # Set lastaid, so I don't have to handle None/uninitialized case.
        # First thing that came to mind was Madoka.  No deep meaning to it.
        self.lastaid = 8069
        self.results = AIDResultsManager()
        self.results['db'] = AIDResults([
            'Title', 'Type', 'Episodes', 'Complete', 'Available',
        ])
        self.results['anidb'] = AIDResults(['Title'])

    @classmethod
    def run_with_file(cls, config, file):
        """Use a file as a script and run commands."""
        animecmd = cls(config, stdin=file)
        animecmd.prompt = ''
        animecmd.cmdloop('')

    def onecmd(self, str):
        # pylint: disable=redefined-builtin,broad-except
        try:
            return super().onecmd(str)
        except CommandError:
            pass
        except Exception:
            traceback.print_exc()

    ###########################################################################
    # Caching
    def purge_cache(self):
        del self.file_picker

    @cached_property
    def file_picker(self) -> FilePicker:
        return FilePicker((PriorityRule(rule.regexp, rule.priority)
                           for rule in self.animedb.priority_rules))

    ###########################################################################
    # Parsing
    def get_aid(self, arg, default_key):
        """Get aid from argument string."""
        if arg == '.':
            return self.lastaid
        else:
            try:
                aid = self.results.parse_aid(arg, default_key=default_key)
            except ValueError as e:
                raise ValueError('Error parsing aid') from e
            else:
                self.lastaid = aid
                return aid


anidb.registry.add_commands(AnimeCmd)
animedb.registry.add_commands(AnimeCmd)
gpl.registry.add_commands(AnimeCmd)
misc.registry.add_commands(AnimeCmd)
watching.registry.add_commands(AnimeCmd)
