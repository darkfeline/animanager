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

import cmd
from textwrap import dedent
import re
import readline  # noqa, needed for readline functionality
import shlex

from animanager import errors
from animanager.constants import VERSION

from . import anidb


class AnimeCmd(cmd.Cmd):

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
        self.anidb = anidb.AniDB(config)
        self.searchdb = anidb.SearchDB(config)

    @classmethod
    def run_with_file(cls, config, file):
        """Use a file as a script and run commands."""
        animecmd = cls(config, stdin=file)
        animecmd.prompt = ''
        animecmd.cmdloop('')

    def default(self, line):
        """Repeat the last command with new arguments."""
        return self.onecmd(' '.join((self.lastcmd, line)))

    ###########################################################################
    # Last command results handling
    last_cmd = None
    last_cmd_results = None

    def _set_last_cmd(self, cmd, results):
        self.last_cmd = cmd
        self.last_cmd_results = results

    def _get_last_cmd(self, cmd):
        if self.last_cmd == cmd:
            return self.last_cmd_results
        else:
            return None

    ###########################################################################
    # quit
    def do_quit(self, arg):
        """Quit."""
        return True

    do_q = do_quit

    def help_q(self):
        print('Alias for "quit".')

    ###########################################################################
    # add
    def do_add(self, arg):
        """Add a series."""
        if not arg:
            self.do_help('add')
        elif arg.isdigit():
            # Handle count.
            results = self._get_last_cmd('add')
            if results is None:
                print('No last search results.')
                return
            aid = results[int(arg)].aid
            self.do_add('#{}'.format(aid))
        elif arg[0] == '#' and arg[1:].isdigit():
            # Handle aid.
            # XXX Handle aid
            pass
        else:
            # Handle search.
            query = re.compile('.*'.join(shlex.split(arg)), re.I)
            results = self.searchdb.search(query)
            width = len(results) % 10 + 1
            template = '{{:{}}} - {{}}'.format(width)
            for i, anime in enumerate(results):
                print(template.format(i, anime.main_title))
            self._set_last_cmd('add', results)

    ###########################################################################
    # watch
    def do_watch(self, arg):
        """Watch series."""
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
