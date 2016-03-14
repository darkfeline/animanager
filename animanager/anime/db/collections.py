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

from collections import namedtuple

EpisodeType = namedtuple(
    'EpisodeType',
    ['id', 'prefix'])

Anime = namedtuple(
    'Anime',
    ['aid', 'title', 'type', 'episodes',
     'watched_episodes', 'complete'
    ])

AnimeFull = namedtuple(
    'AnimeFull',
    ['aid', 'title', 'type', 'episodes', 'startdate', 'enddate'])

AnimeStatus = namedtuple(
    'AnimeStatus',
    ['aid', 'complete', 'watched_episodes'])

WatchingAnime = namedtuple(
    'WatchingAnime',
    ['aid', 'title', 'type', 'episodes', 'regexp'])
