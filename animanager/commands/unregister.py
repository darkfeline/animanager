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
    """Unregister watching regexp for an anime."""
    args = parser.parse_args(args[1:])
    if args.complete:
        query.files.delete_regexp_complete(state.db)
    else:
        if args.aid is None:
            parser.print_help()
        else:
            aid = state.results.parse_aid(args.aid, default_key='db')
            query.files.delete_regexp(state.db, aid)


parser = ArgumentParser(prog='unregister')
parser.add_argument(
    '-c', '--complete', action='store_true',
    help='Unregister all complete anime.')
parser.add_argument('aid', nargs='?', default=None)
