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
import os
import re
# readline is needed for command editing.
import readline  # pylint: disable=unused-import
import shlex
from textwrap import dedent
import traceback

from animanager.constants import VERSION

from . import anidb
from .db import AnimeDB


class AnimeCmd(Cmd):

    # pylint: disable=no-self-use,unused-argument

    intro = dedent('''\
    Animanager {}
    Copyright (C) 2015-2016  Allen Li

    This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
    This is free software, and you are welcome to redistribute it
    under certain conditions; type "gpl c" for details.''').format(VERSION)
    prompt = 'A> '
    use_rawinput = False  # Use readline

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.anidb = anidb.AniDB(config.anime.anidb_cache)
        self.searchdb = anidb.SearchDB(config.anime.anidb_cache)
        self.animedb = AnimeDB(config.anime.database)

    @classmethod
    def run_with_file(cls, config, file):
        """Use a file as a script and run commands."""
        animecmd = cls(config, stdin=file)
        animecmd.prompt = ''
        animecmd.cmdloop('')

    def default(self, line):
        """Repeat the last command with new arguments."""
        return self.onecmd(' '.join((self.lastcmd, line)))

    def onecmd(self, str):
        try:
            return super().onecmd(str)
        except Exception:
            traceback.print_exc()

    ###########################################################################
    # Last command results handling
    last_cmd = None
    last_cmd_results = None

    def _clear_last_cmd(self):
        self.last_cmd = None

    def _set_last_cmd(self, cmd, results):
        self.last_cmd = cmd
        self.last_cmd_results = results

    def _get_last_cmd(self, cmd):
        if self.last_cmd == cmd:
            return self.last_cmd_results
        else:
            return ()

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
    # add
    def do_add(self, arg):
        """Add an anime or update an existing anime."""
        if not arg:
            self.do_help('add')
        elif arg.isdigit():
            self._add_by_count(int(arg))
        elif arg[0] == '#' and arg[1:].isdigit():
            aid = int(arg[1:])
            self._add_by_aid(aid)
        else:
            query = re.compile('.*'.join(shlex.split(arg)), re.I)
            self._add_do_search(query)

    def _add_by_count(self, count):
        results = self._get_last_cmd('add')
        try:
            anime = results[count]
        except IndexError:
            print('Invalid count or stale results.')
        else:
            self._add_by_aid(anime.aid)

    def _add_by_aid(self, aid):
        anime = self.anidb.lookup(aid)
        self.animedb.add(anime)

    def _add_do_search(self, query):
        results = self.searchdb.search(query)
        width = len(results) % 10 + 1
        template = '{{:{}}} - {{}}'.format(width)
        for i, anime in enumerate(results):
            print(template.format(i, anime.main_title))
        self._set_last_cmd('add', results)

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
        results = list(self.animedb.search_anime(query))
        width = len(results) % 10 + 1
        template = '{{:{}}} - {{}}'.format(width)
        for i, anime in enumerate(results):
            print(template.format(i, anime.title))
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
            # Find and show watching anime.
            watchdir = self.config.anime.watchdir
            files = self._find_files(watchdir)
            watching = self.animedb.get_watching()
            pass  # XXX
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

    _gpl_flags = {'c': GPL_COPYING, 'w': GPL_WARRANTY}

    def help_gpl(self):
        print(dedent('''\
        Show GPL information.

        "gpl c" to show copying information.
        "gpl w" to show warranty information.'''))

    def do_gpl(self, arg):
        """Show GPL information."""
        text = self._gpl_flags.get(arg)
        if text:
            print(text)
        else:
            self.do_help('gpl')
