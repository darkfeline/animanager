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

from . import anidb
from . import watchlib
from .db import AnimeDB
from .results import AIDResults
from .results import AIDResultsManager

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

        self.anidb = anidb.AniDB(config.anime.anidb_cache)
        self.searchdb = anidb.SearchDB(config.anime.anidb_cache)
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
    # quit
    def do_quit(self, arg):
        """Quit."""
        return True

    do_q = do_quit

    def help_q(self):
        print('Alias for "quit".')

    ###########################################################################
    # administrative
    def do_purgecache(self, arg):
        """Purge cache tables."""
        self.animedb.cleanup_cache_tables()
        self.animedb.setup_cache_tables()

    ###########################################################################
    # asearch
    def do_asearch(self, arg):
        """Search AniDB."""
        if not arg:
            print('Missing query.')
            return
        query = re.compile('.*'.join(shlex.split(arg)), re.I)
        results = self.searchdb.search(query)
        results = [(anime.aid, anime.main_title) for anime in results]
        self.results['anidb'].set(results)
        self.results['anidb'].print()

    do_as = do_asearch

    def help_as(self):
        print('Alias for asearch.')

    ###########################################################################
    # ashow
    _ashow_msg = dedent("""\
        AID: {}
        Title: {}
        Type: {}
        Episodes: {}
        Start date: {}
        End date: {}\n""")

    def do_ashow(self, arg):
        """Show information about anime in AniDB."""
        arg = shlex.split(arg)[0]
        aid = self.get_aid(arg, default_key='anidb')
        anime = self.anidb.lookup(aid)
        print(self._ashow_msg.format(
            anime.aid,
            anime.title,
            anime.type,
            anime.episodecount,
            anime.startdate,
            anime.enddate,
        ))
        print(tabulate(
                ((episode.epno, episode.title, episode.length)
                 for episode in sorted(
                         anime.episodes,
                         key=lambda x: (x.type, x.number))),
                headers=['Number', 'Title', 'min'],
        ))

    do_ash = do_ashow

    def help_ash(self):
        print('Alias for ashow.')

    ###########################################################################
    # add
    def do_add(self, arg):
        """Add an anime or update an existing anime."""
        arg = shlex.split(arg)[0]
        aid = self.get_aid(arg, default_key='anidb')
        anime = self.anidb.lookup(aid)
        self.animedb.add(anime)

    do_a = do_add

    def help_a(self):
        print('Alias for add.')

    ###########################################################################
    # search
    def do_search(self, arg):
        """Search Animanager database."""
        if not arg:
            print('Missing query.')
            return
        query = '%{}%'.format('%'.join(shlex.split(arg)))
        all_files = watchlib.find_files(self.config.anime.watchdir)
        results = list()
        for anime in self.animedb.search(query):
            anime_files = watchlib.animefiles(anime.regexp)
            anime_files.maybe_add_iter(all_files)
            self.animedb.cache_files(anime.id, anime_files)
            results.append((
                anime.aid, anime.title, anime.type,
                '{}/{}'.format(anime.watched_episodes, anime.episodecount),
                'yes' if anime.complete else '',
                anime_files.available_string(),
            ))
        self.results['db'].set(results)
        self.results['db'].print()

    do_s = do_search

    def help_s(self):
        print('Alias for search.')

    ###########################################################################
    # show
    _show_msg = dedent("""\
        AID: {}
        Title: {}
        Type: {}
        Episodes: {}/{}
        Start date: {}
        End date: {}
        Complete: {}
        {}""")

    def do_show(self, arg):
        """Show anime data."""
        aid, show_episodes = shlex.split(arg)
        aid = self.get_aid(aid, default_key='db')
        anime = self.animedb.lookup(aid, episodes=show_episodes)

        complete_string = 'yes' if anime.complete else 'no'
        if anime.regexp is not None:
            regexp_string = 'Watching regexp: {}\n'.format(anime.regexp)
        else:
            regexp_string = ''
        print(self._show_msg.format(
            anime.aid,
            anime.title,
            anime.type,
            anime.watched_episodes,
            anime.episodecount,
            anime.startdate,
            anime.enddate,
            complete_string,
            regexp_string,
        ))
        if anime.episodes:
            print(tabulate(
                (
                    (self.animedb.get_epno(episode), episode.title, episode.length,
                     'yes' if episode.user_watched else '')
                    for episode in sorted(
                        anime.episodes,
                        key=lambda x: (x.type, x.number))
                ),
                headers=['Number', 'Title', 'min', 'Watched'],
            ))

    do_sh = do_show

    def help_sh(self):
        print('Alias for show.')

    ###########################################################################
    # bump
    def do_bump(self, arg):
        """Bump anime."""
        arg = shlex.split(arg)[0]
        aid = self.get_aid(arg, default_key='db')
        self.animedb.bump(aid)

    do_b = do_bump

    def help_b(self):
        print('Alias for bump.')

    ###########################################################################
    # register
    def do_register(self, arg):
        """Register watching regexp for an anime."""
        args = shlex.split(arg)
        aid = self.get_aid(args.pop(0), default_key='db')
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
        arg = shlex.split(arg)[0]
        aid = self.get_aid(arg, default_key='db')
        self.animedb.delete_regexp(aid)

    do_ur = do_unregister

    def help_ur(self):
        print('Alias for unregister.')

    ###########################################################################
    # watch
    def do_watch(self, arg):
        """Watch an anime."""
        arg = shlex.split(arg)[0]
        aid = self.get_aid(arg, default_key='db')
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

    ###########################################################################
    # GPL information.
    GPL_COPYING = dedent('''\
    Animanager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    Animanager is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public
    License along with this program. If not, see
    <http://www.gnu.org/licenses/gpl.html>.''')

    GPL_WARRANTY = dedent('''\
    Animanager is distributed WITHOUT ANY WARRANTY. The following
    sections from the GNU General Public License, version 3, should
    make that clear.

    15. Disclaimer of Warranty.

    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
    APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT
    WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE
    OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU
    ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

    16. Limitation of Liability.

    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
    CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
    INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES
    ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT
    NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES
    SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO
    OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY
    HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    17. Interpretation of Sections 15 and 16.

    If the disclaimer of warranty and limitation of liability provided
    above cannot be given local legal effect according to their terms,
    reviewing courts shall apply local law that most closely approximates
    an absolute waiver of all civil liability in connection with the
    Program, unless a warranty or assumption of liability accompanies a
    copy of the Program in return for a fee.

    See <http://www.gnu.org/licenses/gpl.html>, for more details.''')

    def help_gpl(self):
        print(dedent('''\
        Show GPL information.

        "gpl c" to show copying information.
        "gpl w" to show warranty information.'''))

    def do_gpl(self, arg):
        """Show GPL information."""
        if arg == 'c':
            print(self.GPL_COPYING)
        elif arg == 'w':
            print(self.GPL_WARRANTY)
        else:
            self.do_help('gpl')
