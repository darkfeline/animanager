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

import pickle
from collections import namedtuple

import animanager.api
import animanager.api.anidb


class TitlesRequest(animanager.api.HTTPRequest):

    """Special AniDB request for titles data."""

    @property
    def request_uri(self):
        return "http://anidb.net/api/anime-titles.xml.gz"

    def open(self):
        response = super().open()
        return TitlesResponse(response)


class TitlesResponse(animanager.api.XMLResponse):

    @property
    def tree_class(self):
        return TitlesTree


SearchEntry = namedtuple('SearchEntry', ['aid', 'main_title', 'titles'])


class TitlesTree(animanager.api.anidb.XMLTree):

    @classmethod
    def load(cls, filename):
        """Load XML tree from pickled file."""
        with open(filename, 'rb') as file:
            return cls(pickle.load(file))

    def dump(self, filename):
        """Dump XML tree into pickled file."""
        with open(filename, 'wb') as file:
            pickle.dump(self.tree, file)

    @staticmethod
    def _get_main_title(anime):
        """Get main title of anime Element."""
        for title in anime:
            if title.attrib['type'] == 'main':
                return title.text

    def search(self, query):
        """Search titles using a compiled RE query."""
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
