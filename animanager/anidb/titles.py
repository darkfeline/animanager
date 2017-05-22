# Copyright (C) 2016-2017  Allen Li
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

"""AniDB titles API.

https://wiki.anidb.net/w/API#Anime_Titles

In the AniDB documentation, this "API" is included with the other APIs,
but it's really just fetching a single XML file with all the titles
data.
"""

import logging
from pathlib import Path
from typing import NamedTuple

from animanager.anidb.anime import get_main_title

import mir.anidb.titles
import mir.cp

logger = logging.getLogger(__name__)


class TitleSearcher:

    """Provides anime title searching, utilizing a local cache."""

    def __init__(self, cachedir: 'str'):
        lib = mir.anidb.titles
        self._titles_getter = lib.CachedTitlesGetter(
            cache=lib.PickleCache(Path(cachedir) / 'anime-titles.pickle'),
            requester=lib.api_requester,
        )

    @mir.cp.NonDataCachedProperty
    def _titles_list(self):
        return self._titles_getter.get()

    def search(self, query: 're.Pattern') -> 'Iterable[_WorkTitles]':
        """Search titles using a compiled RE query."""
        titles: 'Titles'
        for titles in self._titles_list:
            title: 'AnimeTitle'
            for title in titles.titles:
                if query.search(title.title):
                    yield _WorkTitles(
                        aid=titles.aid,
                        main_title=get_main_title(titles.titles),
                        titles=[t.title for t in titles.titles],
                    )
                    continue


class _WorkTitles(NamedTuple):
    aid: int
    main_title: str
    titles: 'List[str]'
