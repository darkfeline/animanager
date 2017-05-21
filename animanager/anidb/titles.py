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

import functools
import logging
import os
import pickle
from urllib.request import urlopen

from animanager.descriptors import CachedProperty
from animanager.xml import XMLTree

from animanager.anidb.http import check_for_errors
from animanager.anidb.http import get_content

from mir.anidb import titles

logger = logging.getLogger(__name__)


def request_titles() -> 'TitlesTree':
    """Request AniDB titles file."""
    response = urlopen('http://anidb.net/api/anime-titles.xml.gz')
    content = get_content(response)
    tree = TitlesTree.fromstring(content)
    check_for_errors(tree)
    return tree


class TitlesTree(XMLTree):

    """XMLTree representation of AniDB anime titles."""

    @classmethod
    def load(cls: 'A', filename: str) -> 'A':
        """Load XML tree from pickled file."""
        with open(filename, 'rb') as file:
            return cls(pickle.load(file))

    def dump(self, filename: str):
        """Dump XML tree into pickled file."""
        with open(filename, 'wb') as file:
            pickle.dump(self.tree, file)

    def search(self, query: 're.Pattern'):
        """Search titles using a compiled RE query."""
        return sorted(_extract_titles(anime)
                      for anime in self._find(query))

    def _find(self, query: 're.Pattern'):
        """Yield anime that match the search query."""
        for anime in self.root:
            for title in anime:
                if query.search(title.text):
                    yield anime
                    break


def _get_main_title(anime: 'Element'):
    """Get main title of anime Element."""
    for title in anime:
        if title.attrib['type'] == 'main':
            return title.text


def _extract_titles(anime: 'Element'):
    return _WorkTitles(
        aid=int(anime.attrib['aid']),
        main_title=_get_main_title(anime),
        titles=[title.text for title in anime],
    )


@functools.total_ordering
class _WorkTitles:

    __slots__ = ('aid', 'main_title', 'titles')

    def __init__(self, aid, main_title, titles):
        self.aid = aid
        self.main_title = main_title
        self.titles = titles

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.aid == other.aid
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.aid < other.aid
        else:
            return NotImplemented


class TitleSearcher:

    """Provides anime title searching, utilizing a local cache.

    Uses a pickle dump of the :class:`TitlesTree` because loading it is
    time consuming.
    """

    def __init__(self, cachedir: 'str'):
        self._cachedir = cachedir
        self._titles_getter = titles.CachedTitlesGetter(
            cache=titles.PickleCache(self._pickle_file),
            requester=titles.api_requester,
        )

    @property
    def _titles_file(self):
        """Anime titles data file path."""
        return os.path.join(self._cachedir, 'anime-titles.xml')

    @property
    def _pickle_file(self):
        """Pickled anime titles data file path."""
        return os.path.join(self._cachedir, 'anime-titles.pickle')

    @CachedProperty
    def titles_tree(self) -> TitlesTree:
        """Titles XML tree."""
        # Try to load pickled file first.
        try:
            titles_tree = TitlesTree.load(self._pickle_file)
        except OSError as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return titles_tree
        if not os.path.exists(self._titles_file):
            # Download titles data if we don't have it.
            titles_tree = self.fetch()
        else:
            titles_tree = TitlesTree.parse(self._titles_file)
        # Dump a pickled file for next time.
        titles_tree.dump(self._pickle_file)
        return titles_tree

    def fetch(self) -> TitlesTree:
        """Fetch fresh titles data from AniDB."""
        try:
            os.unlink(self._pickle_file)
        except OSError:
            pass
        del self.titles_tree
        tree = request_titles()
        tree.write(self._titles_file)
        return tree

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles_tree.search(query)
