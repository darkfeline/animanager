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
from animanager.db import query


def command(state, args):
    """Fix cache issues caused by schema pre-v4."""
    if len(args) > 1:
        print(f'Usage: {args[0]}')
        return
    db = state.db
    _refresh_incomplete_anime(db)
    _fix_cached_completed(db)


def _incomplete_anime(db):
    c = db.cursor()
    c.execute("SELECT DISTINCT aid FROM episode WHERE type=1 AND title LIKE 'Episode %'")
    for row in c:
        yield row[0]
    c.execute("SELECT DISTINCT aid FROM anime WHERE enddate IS NULL")
    for row in c:
        yield row[0]


def _refresh_incomplete_anime(db):
    with db:
        aids = sorted(set(_incomplete_anime(db)))
    for aid in aids:
        anime = request_anime(aid)
        query.update.add(db, anime)
        time.sleep(3)


def _fix_cached_completed(db):
    with db:
        c = db.cursor()
        c.execute("SELECT aid, watched_episodes FROM cache_anime")
        for aid, eps in c:
            c2 = db.cursor()
            c2.execute("UPDATE episode SET user_watched=1 WHERE aid=? AND type=1 AND number<=?",
                       (aid, eps))
