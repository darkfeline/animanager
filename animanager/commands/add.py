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

from animanager.anidb import request_anime
from animanager.db import query


def command(cmd, args):
    """Add an anime from an AniDB search."""
    if len(args) < 2:
        print(f'Usage: {args[0]} {{ID|aid:AID}}')
        return
    aid = cmd.results.parse_aid(args[1], default_key='anidb')
    anime = request_anime(aid)
    query.update.add(cmd.db, anime)
