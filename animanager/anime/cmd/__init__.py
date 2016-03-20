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

from cmd import Cmd
from collections import defaultdict
import logging
import os
import re
# readline is needed for command editing.
import readline  # pylint: disable=unused-import
import shlex
from textwrap import dedent
import traceback

from tabulate import tabulate

from animanager import __version__ as VERSION
from animanager.anime.anidb import AniDB
from animanager.anime.anidb import SearchDB
from animanager.anime import watchlib
from animanager.anime.db import AnimeDB
from animanager.anime.results import AIDResults
from animanager.anime.results import AIDResultsManager

from . import anidb
from . import animedb
from . import gpl
from . import misc

logger = logging.getLogger(__name__)


class AnimeCmd(Cmd):

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
        try:
            return super().onecmd(str)
        except Exception:
            traceback.print_exc()

    ###########################################################################
    # Parsing
    def get_aid(self, arg, default_key=None):
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

    ###########################################################################
    # register
    def do_register(self, arg):
        """Register watching regexp for an anime."""
        args = shlex.split(arg)
        if not args:
            print('Missing AID.')
            return
        aid = args.pop(0)
        aid = self.get_aid(aid, default_key='db')
        if args:
            # Use regexp provided by user.
            pattern = '.*'.join(args)
        else:
            # Make default regexp.
            title = self.animedb.lookup_title(aid)
            # Replace non-word, non-whitespace with whitespace.
            pattern = re.sub(r'[^\w\s]', ' ', title)
            # Split on whitespace and join with wildcard regexp.
            pattern = '.*'.join(re.escape(x) for x in pattern.split())
            # Append episode matching pattern.
            pattern = '.*?'.join((
                pattern,
                r'\b(?P<ep>[0-9]+)(v[0-9]+)?',
            ))
        self.animedb.set_regexp(aid, pattern)

    do_r = do_register

    def help_r(self):
        print('Alias for register.')

    ###########################################################################
    # unregister
    def do_unregister(self, arg):
        """Unregister watching regexp for an anime."""
        args = shlex.split(arg)
        if not args:
            print('Missing AID.')
            return
        aid = args.pop(0)
        aid = self.get_aid(aid, default_key='db')
        self.animedb.delete_regexp(aid)

    do_ur = do_unregister

    def help_ur(self):
        print('Alias for unregister.')

    ###########################################################################
    # watch
    def do_watch(self, arg):
        """Watch an anime."""
        args = shlex.split(arg)
        aid = args.pop(0)
        aid = self.get_aid(arg, default_key='db')
        anime_files = self.animdb.get_files(aid)
        raise NotImplementedError
        if not arg:
            self._watch_list_all()
        elif arg.isdigit():
            # Handle count.
            pass  # XXX
        elif arg[0] == '#' and arg[1:].isdigit():
            # Handle aid.
            pass  # XXX
        else:
            pass  # XXX
        # XXX get watching shows
        # XXX find files
        # XXX match rules
        # XXX play file
        # XXX bump

    def _watch_list_all(self):
        # Find files.
        watchdir = self.config.anime.watchdir
        files = self._find_files(watchdir)

        # Associate files with watching anime.
        watching_list = self.animedb.get_watching()
        anime_files = dict((anime.aid, defaultdict(list)) for anime in watching_list)
        for filename in files:
            for anime in watching_list:
                match = anime.regexp.search(os.path.basename(filename))
                if match:
                    try:
                        ep = int(match.group('ep'))
                    except ValueError:
                        logger.error(
                            'Invalid episode matched using %s for %s',
                            anime.title, filename)
                        continue
                    anime_files[anime.aid][ep].append(files)
                    break

        # Print
        pass  # XXX

anidb.registry.add_commands(AnimeCmd)
animedb.registry.add_commands(AnimeCmd)
gpl.registry.add_commands(AnimeCmd)
misc.registry.add_commands(AnimeCmd)
