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

import itertools
import os
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List, Sequence
from typing.re import Pattern


def find_files(dirpath: str, test: Callable[[str], Any]) -> Iterable[str]:
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
    def maybe_add(self, filename: str) -> None:
        pass

    @abstractmethod
    def maybe_add_iter(self, filenames: Iterable[str]) -> None:
        pass

    @abstractmethod
    def to_json(self):
        return '{}'

    @classmethod
    @abstractmethod
    def from_json(cls, string):
        return cls()


class PriorityRule(tuple):

    __slots__ = ()

    def __new__(cls, regexp: str, priority: int) -> 'PriorityRule':
        compiled_regexp = re.compile(regexp, re.I)
        return super().__new__(cls, (compiled_regexp, priority))

    @property
    def regexp(self) -> Pattern:
        return self[0]

    @property
    def priority(self) -> int:
        return self[1]


class FilePicker:

    """Class for picking one file out of many based on priority rules."""

    def __init__(self, rules: Iterable[PriorityRule]) -> None:
        self.rules = defaultdict(list)  # type: Dict[int, List[Pattern]]
        for rule in rules:
            self.rules[rule.priority].append(rule.regexp)

    def pick(self, filenames: Sequence[str]) -> str:
        """Pick one filename based on priority rules."""
        for priority in sorted(self.rules.keys(), reverse=True):
            patterns = self.rules[priority]
            for pattern in patterns:
                for filename in filenames:
                    if pattern.search(filename):
                        return filename
        return filenames[0]
