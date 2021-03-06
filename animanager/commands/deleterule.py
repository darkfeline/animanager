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
    """Delete priority rule."""
    args = parser.parse_args(args[1:])
    query.files.delete_priority_rule(state.db, args.id)
    del state.file_picker


parser = ArgumentParser(prog='deleterule')
parser.add_argument('id', type=int)
