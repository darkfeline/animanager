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

import logging

from animanager.date import timestamp
from animanager.sqlite.utils import upsert

from .eptype import get_eptype
from .select import lookup
from .status import cache_status, set_status

logger = logging.getLogger(__name__)


def add(db, anime):
    """Add an anime (or update existing).

    anime is an AnimeTree instance.

    """
    values = {
        'aid': anime.aid,
        'title': anime.title,
        'type': anime.type,
        'episodecount': anime.episodecount,
        'startdate': anime.startdate,
        'enddate': anime.enddate,
    }
    if anime.startdate is not None:
        values['startdate'] = timestamp(anime.startdate)
    if anime.enddate is not None:
        values['enddate'] = timestamp(anime.enddate)
    with db:
        upsert(db, 'anime', ['aid'], values)
        for episode in anime.episodes:
            add_episode(db, anime.aid, episode)


def add_episode(db, aid, episode):
    """Add an episode."""
    values = {
        'aid': aid,
        'type': episode.type,
        'number': episode.number,
        'title': episode.title,
        'length': episode.length,
    }
    upsert(db, 'episode', ['aid', 'type', 'number'], values)


def set_watched(db, aid, ep_type, number):
    """Set episode as watched."""
    db.cursor().execute(
        """UPDATE episode SET user_watched=:watched
        WHERE aid=:aid AND type=:type AND number=:number""",
        {
            'aid': aid,
            'type': ep_type,
            'number': number,
            'watched': 1,
        })


def bump(db, aid):
    """Bump anime regular episode count."""
    anime = lookup(db, aid)
    if anime.complete:
        return
    episode = anime.watched_episodes + 1
    with db:
        set_watched(db, aid, get_eptype(db, 'regular').id, episode)
        set_status(
            db, aid,
            anime.enddate and episode >= anime.episodecount,
            episode)


def reset(db, aid, episode):
    """Reset episode count for anime."""
    params = {
        'aid': aid,
        'type': get_eptype(db, 'regular').id,
        'watched': 1,
        'number': episode,
    }
    with db:
        cur = db.cursor()
        cur.execute(
            """UPDATE episode SET user_watched=:watched
            WHERE aid=:aid AND type=:type AND number<=:number""",
            params)
        params['watched'] = 0
        cur.execute(
            """UPDATE episode SET user_watched=:watched
            WHERE aid=:aid AND type=:type AND number>:number""",
            params)
        cache_status(db, aid, force=True)
