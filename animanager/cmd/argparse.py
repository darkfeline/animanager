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

from .errors import CommandExit


class ArgumentParser(argparse.ArgumentParser):

    """ArgumentParser customized for Animanager's CLI."""

    def __init__(self, *args, **kwargs):
        add_help = kwargs.pop('add_help', False)
        super().__init__(self, *args, add_help=add_help, **kwargs)

    def exit(self, status=0, message=None):
        """Override SystemExit."""
        if message is not None:
            print(message)
        raise CommandExit()

    def error(self, message):
        """Override printing to stderr."""
        print(message)
        self.print_help()
        raise CommandExit()

    def add_aid(self):
        self.add_argument('aid')

    def add_query(self):
        """Add a generic query argument."""
        self.add_argument('query', nargs=argparse.REMAINDER)
