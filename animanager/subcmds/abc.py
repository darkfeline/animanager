# Copyright (C) 2015-2016  Allen Li
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

"""This module contains ABCs for subcommands."""

from abc import ABC, abstractmethod

__all__ = ['Subcommand']


class Subcommand(ABC):

    """Interface for adding subcommand parsers to argparse.ArgumentParser"""

    # pylint: disable=too-few-public-methods

    @classmethod
    @abstractmethod
    def setup_parser(cls, subparsers):
        """Setup parser with subcommand."""
