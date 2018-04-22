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

"""AniDB API bindings."""

import os
import re
from typing import NamedTuple

from mir.anidb import api
import mir.anidb.anime as alib
import mir.anidb.titles as tlib
import mir.cp

_CLIENT = api.Client(
    name='kfanimanager',
    version=1,
)


def request_anime(aid: int) -> 'Anime':
    """Make an anime API request."""
    anime_info = alib.request_anime(_CLIENT, aid)
    return Anime._make(anime_info)


class Anime(alib.Anime):

    @property
    def title(self) -> str:
        return _get_main_title(self.titles)

    @property
    def episodes(self) -> 'Tuple[Episode]':
        return tuple(Episode._make(ep)
                     for ep in alib.Anime.episodes.fget(self))


class Episode(alib.Episode):

    _NUMBER_SUFFIX = re.compile(r'(\d+)$')

    @property
    def number(self) -> int:
        """Episode number.

        Unique for an anime and episode type, but not unique across episode
        types for the same anime.
        """
        match = self._NUMBER_SUFFIX.search(self.epno)
        return int(match.group(1))

    @property
    def title(self) -> str:
        """Episode title."""
        for title in self.titles:
            if title.lang == 'ja':
                return title.title
        # In case there's no Japanese title.
        return self.titles[0].title


class TitleSearcher:

    """Provides anime title searching, utilizing a local cache."""

    def __init__(self, cachedir):
        self._cache = tlib.PickleCache(os.path.join(cachedir, 'anime-titles.pickle'))

    @mir.cp.NonDataCachedProperty
    def _titles_list(self):
        try:
            return self._cache.load()
        except tlib.CacheMissingError:
            titles = tlib.request_titles()
            self._cache.save(titles)
            return titles

    def search(self, query: 're.Pattern') -> 'Iterable[_WorkTitles]':
        """Search titles using a compiled RE query."""
        titles: 'Titles'
        for titles in self._titles_list:
            title: 'AnimeTitle'
            for title in titles.titles:
                if query.search(title.title):
                    yield WorkTitles(
                        aid=titles.aid,
                        main_title=_get_main_title(titles.titles),
                        titles=[t.title for t in titles.titles],
                    )
                    continue


class WorkTitles(NamedTuple):
    aid: int
    main_title: str
    titles: 'List[str]'


def _get_main_title(titles: 'Iterable[AnimeTitle]'):
    for title in titles:
        if title.type == 'main':
            return title.title
