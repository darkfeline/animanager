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

import time

from animanager.anidb import request_anime
from animanager.cmdlib import ArgumentParser
from animanager.db import query


def command(cmd, args):
    """Add an anime from an AniDB search."""
    args = parser.parse_args(args[1:])
    if args.watching:
        rows = query.select.select(cmd.db, 'regexp IS NOT NULL', [], ['aid'])
        aids = [anime.aid for anime in rows]
    elif args.incomplete:
        rows = query.select.select(cmd.db, 'enddate IS NULL', [], ['aid'])
        aids = [anime.aid for anime in rows]
    else:
        aid = cmd.results.parse_aid(args.aid, default_key='db')
        aids = [aid]
    if not aids:
        return
    anime = request_anime(aids.pop())
    query.update.add(cmd.db, anime)
    print('Updated {} {}'.format(anime.aid, anime.title))
    for aid in aids:
        time.sleep(2)
        anime = request_anime(aid)
        query.update.add(cmd.db, anime)
        print('Updated {} {}'.format(anime.aid, anime.title))


parser = ArgumentParser(prog='update')
parser.add_argument('aid', nargs='?', default=None)
parser.add_argument(
    '-i', '--incomplete', action='store_true',
    help='Update all incomplete anime.')
parser.add_argument(
    '-w', '--watching', action='store_true',
    help='Update all watching anime.')
