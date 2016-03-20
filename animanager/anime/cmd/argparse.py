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


import argparse
import shlex
import re


class ArgumentParser(argparse.ArgumentParser):

    @property
    def parsing(self):
        """Decorator to parse command arguments."""
        def decorate(func):
            def parse_args_around(self, arg):
                args = self.parse_args(shlex.split(arg))
                return func(self, args)
            return parse_args_around
        return decorate

    def exit(self, status=0, message=None):
        """Override SystemExit."""
        if message:
            print(message)

    def error(self, message):
        """Override printing to stderr."""
        print(message)

    def add_re_query(self):
        self.add_argument(
            'query',
            nargs=argparse.REMAINDER,
            type=self._compile_re_query,
        )

    @staticmethod
    def _compile_re_query(args):
        return re.compile('.*'.join(args), re.I)

    def add_sql_query(self):
        self.add_argument(
            'query',
            nargs=argparse.REMAINDER,
            type=self._compile_sql_query,
        )

    @staticmethod
    def _compile_sql_query(args):
        return '%{}%'.format('%'.join(args))

    def add_aid(self):
        self.add_argument('aid')


re_query_parser = ArgumentParser()
re_query_parser.add_re_query()


sql_query_parser = ArgumentParser()
sql_query_parser.add_sql_query()

aid_parser = ArgumentParser()
aid_parser.add_aid()
