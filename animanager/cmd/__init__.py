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
import readline
from inspect import cleandoc

del readline
logger = logging.getLogger(__name__)


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


class CmdExit(Exception):
    """Exception for exiting CLI."""
