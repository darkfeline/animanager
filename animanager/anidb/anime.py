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

"""AniDB HTTP anime API."""

import re

from mir.anidb import api
from mir.anidb import anime

_CLIENT = 'kfanimanager'
_CLIENTVER = 1

_client = api.Client(
    name=_CLIENT,
    version=_CLIENTVER,
)


def request_anime(aid: int) -> 'AnimeTree':
    """Make an anime API request."""
    anime_info = anime.request_anime(_client, aid)
    return _rewrap_anime(anime_info)


def _rewrap_anime(anime_tuple):
    """Replace anime.Anime tuple with an instance of our subclass."""
    return Anime._make(anime_tuple)


class Anime(anime.Anime):

    @property
    def title(self) -> str:
        """Main title."""
        return get_main_title(self.titles)

    @property
    def episodes(self) -> 'Tuple[Episode]':
        """The anime's episodes."""
        return tuple(Episode._make(ep)
                     for ep in anime.Anime.episodes.fget(self))


def get_main_title(titles: 'Iterable[AnimeTitle]'):
    for title in titles:
        if title.type == 'main':
            return title.title


class Episode(anime.Episode):

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
