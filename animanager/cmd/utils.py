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

import re
import typing
from typing import Iterable

Pattern = typing.re.Pattern


def compile_re_query(args: Iterable[str]) -> Pattern:
    return re.compile('.*'.join(args), re.I)


def compile_sql_query(args: Iterable[str]) -> str:
    return '%{}%'.format('%'.join(args))
