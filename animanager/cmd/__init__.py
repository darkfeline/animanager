# Copyright (C) 2016, 2017  Allen Li
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

"""This package contains tools for constructing custom Cmd, command line
interface classes.

"""

import argparse
import logging
import readline  # pylint: disable=unused-import
import shlex
from inspect import cleandoc

from .utils import compile_re_query

logger = logging.getLogger(__name__)


class Cmd:

    """Our CLI class."""

    prompt = '> '
    intro = ''
    commands = {}
    safe_exceptions = set()

    def __init__(self):
        self.last_cmd = []

    def cmdloop(self):
        """Start CLI REPL."""
        print(self.intro)
        stop = False
        while not stop:
            cmdline = input(self.prompt)
            tokens = shlex.split(cmdline)
            if not tokens:
                if self.last_cmd:
                    tokens = self.last_cmd
                else:
                    print('No previous command.')
                    continue
            try:
                command = self.commands[tokens[0]]
            except KeyError:
                print('Invalid command.')
                continue
            else:
                self.last_cmd = tokens
            try:
                stop = command(self, *tokens[1:])
            except ParseExit:
                continue
            except Exception as e:
                if e not in self.safe_exceptions:
                    logger.exception('Error!')


class Command:

    """A CLI command."""

    def __init__(self, parser, func):
        self.parser = parser
        self.func = func
        if parser.description is None:
            self.parser.description = cleandoc(self.func.__doc__)

    def __call__(self, cmd, *args):
        args = self.parser.parse_args(args)
        return self.func(cmd, args)


class StateCommand:

    """Alternative command that takes CmdState instead of Cmd.

    This is used to rewrite code to use CmdState.
    """

    def __init__(self, parser, func):
        self.parser = parser
        self.func = func
        if parser.description is None:
            self.parser.description = cleandoc(self.func.__doc__)

    def __call__(self, cmd, *args):
        args = self.parser.parse_args(args)
        return self.func(cmd.state, args)


class ArgumentParser(argparse.ArgumentParser):

    """ArgumentParser customized for Animanager's CLI."""

    def exit(self, status=0, message=None):
        """Override SystemExit."""
        if message is not None:
            print(message)
        raise ParseExit()

    def error(self, message):
        """Override printing to stderr."""
        print(message)
        self.print_help()
        raise ParseExit()


class ParseExit(Exception):
    """This is used to exit parsing in lieu of sys.exit()"""
