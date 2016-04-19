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
from functools import lru_cache

from animanager.api import anidb

logger = logging.getLogger(__name__)


class AniDB:

    """Provides access to AniDB data, via cache and API."""

    def lookup(self, aid):
        """Look up given AID.

        Uses cache if available.

        """
        return anidb.request_anime(aid)


class SearchDB:

    """Provides access to local cache of AniDB titles data.

    The titles data is used for searching.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    @property
    @lru_cache(None)
    def titles_file(self):
        return os.path.join(self.cachedir, 'anime-titles.xml')

    @property
    @lru_cache(None)
    def pickle_file(self):
        return os.path.join(self.cachedir, 'anime-titles.pickle')

    @property
    @lru_cache(None)
    def titles_tree(self) -> anidb.TitlesTree:
        return self.load_tree()

    def load_tree(self) -> anidb.TitlesTree:
        # Try to load from pickled file courageously.
        try:
            titles_tree = anidb.TitlesTree.load(self.pickle_file)
        except Exception as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return titles_tree
        # Download titles data if we don't have it.
        if not os.path.exists(self.titles_file):
            titles_tree = self.fetch()
        else:
            titles_tree = anidb.TitlesTree.parse(self.titles_file)
        # Dump a pickled file for next time.
        titles_tree.dump(self.pickle_file)
        return titles_tree

    def fetch(self) -> anidb.TitlesTree:
        """Fetch fresh titles data from AniDB."""
        try:
            os.unlink(self.pickle_file)
        except OSError:
            pass
        tree = anidb.request_titles()
        tree.write(self.titles_file)
        return tree

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles_tree.search(query)
