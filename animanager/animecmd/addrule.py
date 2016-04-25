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

from animanager.cmd import ArgumentParser, Command
from animanager.db import query

parser = ArgumentParser(prog='addrule')
parser.add_argument('regexp')
parser.add_argument('priority', nargs='?', default=None, type=int)

def func(cmd, args):
    """Add a priority rule for files."""
    row_id = query.files.add_priority_rule(cmd.db, args.regexp, args.priority)
    del cmd.file_picker
    print('Added rule {}'.format(row_id))

command = Command(parser, func)
