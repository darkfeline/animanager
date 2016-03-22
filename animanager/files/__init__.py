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

from abc import ABC
from abc import abstractmethod
import os


def find_files(dirpath, test):
    """Find all files, filtered by test function.

    Returns a generator that yields paths in no particular order.

    """
    for dirpath, _, filenames in os.walk(dirpath):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if test(filepath):
                yield filepath


class BaseFiles(ABC):

    """Interface for collections of files."""

    @abstractmethod
    def maybe_add(self, filename):
        pass

    @abstractmethod
    def maybe_add_iter(self, filenames):
        pass