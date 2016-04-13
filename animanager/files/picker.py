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

import re
from collections import defaultdict
import typing
from typing import Iterable, Sequence

__all__ = ['PriorityRule', 'FilePicker']

Pattern = typing.re.Pattern


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
        # Maps priority int to lists of regexp patterns.
        self.rules = defaultdict(list)
        for rule in rules:
            self.rules[rule.priority].append(rule.regexp)

    def pick(self, filenames: Sequence[str]) -> str:
        """Pick one filename based on priority rules."""
        filenames = sorted(filenames, reverse=True)  # e.g., v2 before v1
        for priority in sorted(self.rules.keys(), reverse=True):
            patterns = self.rules[priority]
            for pattern in patterns:
                for filename in filenames:
                    if pattern.search(filename):
                        return filename
        return filenames[0]
