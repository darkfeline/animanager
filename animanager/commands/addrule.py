# Copyright (C) 2018  Allen Li
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

from animanager.cmdlib import ArgumentParser
from animanager.db import query


def command(state, args):
    """Add a priority rule for files."""
    args = parser.parse_args(args[1:])
    row_id = query.files.add_priority_rule(state.db, args.regexp, args.priority)
    del state.file_picker
    print('Added rule {}'.format(row_id))


parser = ArgumentParser(prog='addrule')
parser.add_argument('regexp')
parser.add_argument('priority', nargs='?', default=None, type=int)
