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

import logging
import os

from . import anime
from . import titles

logger = logging.getLogger(__name__)


class AniDB:

    """Provides access to AniDB data, via cache and API."""

    def __init__(self, cachedir):
        self.cache = anime.AnimeCache(cachedir)

    def lookup(self, aid):
        """Look up given AID.

        Uses cache if available.

        """
        if self.cache.has(aid):
            return self.cache.retrieve(aid)
        else:
            request = anime.AnimeRequest(aid)
            response = request.open()
            return response.xml()


class SearchDB:

    """Provides access to local cache of AniDB titles data.

    The titles data is used for searching.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir
        self._titles = None

    @property
    def titles(self):
        if self._titles is None:
            self.load_tree()
        return self._titles

    def load_tree(self):
        pickle_file = os.path.join(self.cachedir, 'anime-titles.pickle')
        # Try to load from pickled file courageously.
        try:
            self._titles = titles.TitlesTree.load(pickle_file)
        except Exception as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return
        titles_file = os.path.join(self.cachedir, 'anime-titles.xml')
        # Download titles data if we don't have it.
        if not os.path.exists(titles_file):
            request = titles.TitlesRequest()
            response = request.open()
            self._titles = response.xml()
        else:
            self._titles = titles.TitlesTree.parse(titles_file)
        # Dump a pickled file for next time.
        self.titles.dump(pickle_file)

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles.search(query)
