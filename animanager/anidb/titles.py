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

"""AniDB titles API.

In the `AniDB documentation <https://wiki.anidb.net/w/API#Anime_Titles>`_, it's
included with the APIs, but it's really just fetching a single XML file with
all the titles data.

"""

import logging
import os
import pickle
from collections import namedtuple
from typing import List
from urllib.request import urlopen

from animanager.descriptors import CachedProperty
from animanager.xml import XMLTree

from .http import check_for_errors, get_content

logger = logging.getLogger(__name__)


def request_titles() -> 'TitlesTree':
    """Request AniDB titles file.

    :returns: AniDB titles data
    :rtype: TitlesTree

    """
    response = urlopen('http://anidb.net/api/anime-titles.xml.gz')
    content = get_content(response)
    tree = TitlesTree.fromstring(content)
    check_for_errors(tree)
    return tree


SearchEntry = namedtuple('SearchEntry', ['aid', 'main_title', 'titles'])
"""Represents one anime in the titles data."""


class TitlesTree(XMLTree):

    """XMLTree representation of AniDB anime titles."""

    @classmethod
    def load(cls, filename: str) -> 'TitlesTree':
        """Load XML tree from pickled file.

        :param str filename: file path
        :returns: anime titles
        :rtype: TitlesTree

        """
        with open(filename, 'rb') as file:
            return cls(pickle.load(file))

    def dump(self, filename: str):
        """Dump XML tree into pickled file.

        :param str filename: file path

        """
        with open(filename, 'wb') as file:
            pickle.dump(self.tree, file)

    @staticmethod
    def _get_main_title(anime):
        """Get main title of anime Element."""
        for title in anime:
            if title.attrib['type'] == 'main':
                return title.text

    def search(self, query) -> List['SearchEntry']:
        """Search titles using a compiled RE query.

        :returns: list of matching anime
        :rtype: list

        """
        found = []
        for anime in self.root:
            for title in anime:
                if query.search(title.text):
                    aid = int(anime.attrib['aid'])
                    main_title = self._get_main_title(anime)
                    titles = [title.text for title in anime]
                    found.append(SearchEntry(aid, main_title, titles))
                    break
        return sorted(found, key=lambda anime: anime.aid)


class TitleSearcher:

    """Provides anime title searching, utilizing a local cache.

    Uses a pickle dump of the :class:`TitlesTree` because loading it is
    time consuming.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    @CachedProperty
    def titles_file(self):
        """Anime titles data file path."""
        return os.path.join(self.cachedir, 'anime-titles.xml')

    @CachedProperty
    def pickle_file(self):
        """Pickled anime titles data file path."""
        return os.path.join(self.cachedir, 'anime-titles.pickle')

    @CachedProperty
    def titles_tree(self) -> TitlesTree:
        """Titles XML tree."""
        # Try to load pickled file first.
        try:
            titles_tree = TitlesTree.load(self.pickle_file)
        except OSError as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return titles_tree
        if not os.path.exists(self.titles_file):
            # Download titles data if we don't have it.
            titles_tree = self.fetch()
        else:
            titles_tree = TitlesTree.parse(self.titles_file)
        # Dump a pickled file for next time.
        titles_tree.dump(self.pickle_file)
        return titles_tree

    def fetch(self) -> TitlesTree:
        """Fetch fresh titles data from AniDB."""
        try:
            os.unlink(self.pickle_file)
        except OSError:
            pass
        del self.titles_tree
        tree = request_titles()
        tree.write(self.titles_file)
        return tree

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles_tree.search(query)
