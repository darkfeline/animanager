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

"""Shared collection types used by queries."""

from dataclasses import dataclass


@dataclass
class Anime:
    aid: int
    title: str
    type: str
    episodecount: int
    startdate: int
    enddate: int
    watched_episodes: int
    complete: bool
    regexp: str
    episodes: 'List[Episode]' = ()


@dataclass
class Episode:
    aid: int
    type: str
    number: int
    title: str
    length: int
    user_watched: bool
