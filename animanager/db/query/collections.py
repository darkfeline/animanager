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
    aid: int = 0
    title: str = ''
    type: str = ''
    episodecount: int = 0
    startdate: int = 0
    enddate: int = 0
    watched_episodes: int = 0
    complete: bool = False
    regexp: str = ''
    episodes: 'List[Episode]' = ()


@dataclass
class Episode:
    aid: int = 0
    type: str = ''
    number: int = 0
    title: str = ''
    length: int = 0
    user_watched: bool = False
