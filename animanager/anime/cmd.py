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

from animanager.constants import VERSION

from . import anidb
from .db import AnimeDB

logger = logging.getLogger(__name__)


class SearchResults:

    """Class for managing search results for commands to access.

    >>> SearchResults(['title'])
    SearchResults(['title'], [])

    >>> SearchResults(['title'], [('Konosuba',), ('Oreimo',)])
    SearchResults(['title'], [('Konosuba',), ('Oreimo',)])

    """

    def __init__(self, headers, results=None):
        self.headers = ['#'] + headers
        if results is None:
            self.results = list()
        else:
            self.results = results

    def __repr__(self):
        return 'SearchResults({}, {})'.format(
            self.headers[1:],
            self.results
        )

    def set(self, results):
        """Set results.

        results is an iterable of tuples, where each tuple is a row of results.

        >>> x = SearchResults(['title'])
        >>> x.set([('Konosuba',), ('Oreimo',)])
        >>> x
        SearchResults(['title'], [('Konosuba',), ('Oreimo',)])

        """
        self.results = list(results)

    def get(self, number):
        """Get a result row.

        results are indexed from 1.

        >>> SearchResults(['title'], [('Konosuba',), ('Oreimo',)]).get(1)
        ('Konosuba',)

        """
        return self.results[number - 1]

    def print(self):
        """Print results table."""
        print(tabulate(
            ((i, *row) for i, row in enumerate(self.results, 1)),
            headers=self.headers,
        ))


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
        self.results = SearchResults([
            'AID', 'Title', 'Type', 'Episodes', 'Complete',
        ])
        self.aresults = SearchResults(['AID', 'Title'])

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
    def parse_aid(self, text, aresults=False):
        """Parse argument text for aid.

        May retrieve the aid from search result tables as necessary.  aresults
        determines which search results to use by default; True means aresults
        is the default.

        The accepted formats, in order:

        Explicit AID:              aid:12345
        Explicit results number:   #:12
        Explicit aresults number:  a#:12
        Default results number:    12

        """
        if text.startswith('aid:'):
            return int(text[len('aid:'):])
        elif text.startswith('#:'):
            number = int(text[len('#:'):])
            return self.results.get(number)[0]
        elif text.startswith('a#:'):
            number = int(text[len('a#:'):])
            return self.aresults.get(number)[0]
        else:
            number = int(text)
            if aresults:
                return self.aresults.get(number)[0]
            else:
                return self.results.get(number)[0]

    def get_aid(self, arg, aresults=False):
        """Get aid from argument string.

        This extends parse_aid() with lastaid handling and other user-friendly
        features.  parse_aid() is kept separate for testing and modularity.

        """
        if arg:
            try:
                aid = self.parse_aid(arg, aresults=aresults)
            except IndexError as e:
                logger.debug('Error parsing aid: %s', e)
                print('Error parsing aid.')
            self.lastaid = aid
        else:
            aid = self.lastaid
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
        self.aresults.set(results)
        self.aresults.print()

    do_as = do_asearch

    def help_as(self):
        print('Alias for asearch.')

    ###########################################################################
    # ashow
    def do_ashow(self, arg):
        """Show information about anime in AniDB."""
        aid = self.get_aid(arg, aresults=True)
        anime = self.anidb.lookup(aid)

        print('AID: {}'.format(anime.aid))
        print('Title: {}'.format(anime.title))
        print('Type: {}'.format(anime.type))
        print('Episodes: {}'.format(anime.episodecount))
        print('Start date: {}'.format(anime.startdate))
        print('End date: {}\n'.format(anime.enddate))

        print(tabulate(
            [
                (episode.epno, episode.title, episode.length)
                for episode in sorted(
                     anime.episodes,
                     key=lambda x: (x.type, x.number))
            ],
            headers=['Number', 'Title', 'min'],
        ))

    do_ash = do_ashow

    def help_ash(self):
        print('Alias for ashow.')

    ###########################################################################
    # add
    def do_add(self, arg):
        """Add an anime or update an existing anime."""
        aid = self.get_aid(arg, aresults=True)
        anime = self.anidb.lookup(aid)
        self.animedb.add(anime)

    ###########################################################################
    # search
    def do_search(self, arg):
        """Search Animanager database."""
        if not arg:
            print('Missing query.')
            return
        query = '%{}%'.format('%'.join(shlex.split(arg)))
        results = self.animedb.search(query)
        results = [
            (anime.aid, anime.title, anime.type,
             '{}/{}'.format(anime.watched_episodes, anime.episodes),
             'yes' if anime.complete else '')
            for anime in results
        ]
        self.results.set(results)
        self.results.print()

    do_s = do_search

    def help_s(self):
        print('Alias for search.')

    ###########################################################################
    # show
    def do_show(self, arg):
        """Show anime data."""
        # XXX
        aid = self.get_aid(arg, aresults=True)
        anime = self.anidb.lookup(aid)

        print('AID: {}'.format(anime.aid))
        print('Title: {}'.format(anime.title))
        print('Type: {}'.format(anime.type))
        print('Episodes: {}'.format(anime.episodecount))
        print('Start date: {}'.format(anime.startdate))
        print('End date: {}\n'.format(anime.enddate))

        print(tabulate(
            [
                (episode.epno, episode.title, episode.length)
                for episode in sorted(
                     anime.episodes,
                     key=lambda x: (x.type, x.number))
            ],
            headers=['Number', 'Title', 'min'],
        ))

    do_sh = do_show

    def help_sh(self):
        print('Alias for show.')

    ###########################################################################
    # bump
    def do_bump(self, arg):
        """Bump anime."""
        if not arg:
            self.do_help('bump')
        elif arg.isdigit():
            self._bump_by_count(int(arg))
        elif arg[0] == '#' and arg[1:].isdigit():
            aid = int(arg[1:])
            self._bump_by_aid(aid)
        else:
            query = '%{}%'.format('%'.join(shlex.split(arg)))
            self._bump_do_search(query)

    def _bump_by_count(self, count):
        results = self._get_last_cmd('bump')
        try:
            anime = results[count]
        except IndexError:
            print('Invalid count or stale results.')
        else:
            self._bump_by_aid(anime.aid)

    def _bump_by_aid(self, aid):
        self.animedb.bump(aid)

    def _bump_do_search(self, query):
        results = [anime.title for anime in self.animedb.search_anime(query)]
        self._print_results(results)
        self._set_last_cmd('bump', results)

    ###########################################################################
    # watch
    @staticmethod
    def _is_video(filename):
        """Return whether the filename is a video file."""
        extension = os.path.splitext(filename)[1]
        return extension in ('.mkv', '.mp4', '.avi')

    def _find_files(self, watchdir):
        """Find video files to watch."""
        files = []
        for dirpath, _, filenames in os.walk(watchdir):
            # Skip the trash directory.
            if os.stat(dirpath) == os.stat(self.config.anime.trashdir):
                continue
            for filename in filenames:
                if self._is_video(filename):
                    files.append(os.path.join(dirpath, filename))
        return sorted(files)

    def do_watch(self, arg):
        """Watch an anime."""
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
