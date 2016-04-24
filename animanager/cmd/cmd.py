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

import readline  # pylint: disable=unused-import
import shlex
import traceback
from itertools import chain

from animanager.utils import HybridMethod

from .argparse import ParseExit


class Cmd:

    """Our CLI class."""

    prompt = '> '
    intro = ''
    commands = {}

    def __init__(self):
        self.commands = {}

    def runloop(self):
        """Start CLI REPL."""
        # pylint: disable=broad-except
        stop = False
        while not stop:
            cmdline = input(self.prompt)
            tokens = shlex.split(cmdline)
            try:
                command = self.commands[tokens.pop(0)]
            except KeyError:
                print('Invalid command.\n\nCommands: {}'.format(
                    ', '.join(sorted(self.commands))
                ))
            try:
                stop = command(self, tokens)
            except ParseExit:
                continue
            except Exception:
                traceback.print_exc()

    @classmethod
    def _add_class_command(cls, command, name, *names):
        """Add a command."""
        for name in chain([name], names):
            cls.commands[name] = command

    def _add_instance_command(self, command, name, *names):
        """Add a command."""
        for name in chain([name], names):
            self.commands[name] = command

    add_command = HybridMethod(_add_class_command, _add_instance_command)


class Command:

    """A CLI command."""

    # pylint: disable=too-few-public-methods

    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, cmd, *args):
        args = self.parser.parse_args(args)
        return self.func(cmd, args)
