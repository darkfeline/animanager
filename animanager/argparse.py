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

"""Custom argument parsing."""

import argparse
import functools
import re
import shlex
from typing import Iterable
from typing.re import Pattern


class ArgumentParser(argparse.ArgumentParser):

    """ArgumentParser customized for Animanager's CLI."""

    def error(self, message):
        """Override printing to stderr."""
        print(message)
        self.print_help()
        raise CommandError()

    @property
    def parsing(self):
        """Decorator to parse command arguments.

        This decorates a cmd.Cmd command method do_foo(self, arg) by splitting
        its single argument string into tokens, parsing it via ArgumentParser,
        then calling the original function with the parsed args.

        """
        def decorate(func):
            @functools.wraps(func)
            def parse_args_around(self2, arg):
                args = self.parse_args(shlex.split(arg))
                return func(self2, args)
            return parse_args_around
        return decorate

    def add_query(self):
        self.add_argument('query', nargs=argparse.REMAINDER)


def compile_re_query(args: Iterable[str]) -> Pattern:
    return re.compile('.*'.join(args), re.I)


def compile_sql_query(args: Iterable[str]) -> str:
    return '%{}%'.format('%'.join(args))

class CommandError(Exception):
    """Error parsing command arguments."""
