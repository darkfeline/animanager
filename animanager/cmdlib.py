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

logger = logging.getLogger(__name__)


class ArgumentParser(argparse.ArgumentParser):

    """Modified to not exit."""

    def exit(self, status=0, message=None):
        if message is not None:
            print(message)
        raise CmdExit()

    def error(self, message):
        print(message)
        self.print_help()
        raise CmdExit()


class CmdExit(Exception):
    """Exception for exiting CLI."""
