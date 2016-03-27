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

from animanager.api.anidb import AnimeRequest, TitlesRequest, TitlesTree
from animanager.cache import cached_property

logger = logging.getLogger(__name__)


class AniDB:

    """Provides access to AniDB data, via cache and API."""

    def lookup(self, aid):
        """Look up given AID.

        Uses cache if available.

        """
        request = AnimeRequest(aid)
        response = request.open()
        tree = response.xml()
        return tree


class SearchDB:

    """Provides access to local cache of AniDB titles data.

    The titles data is used for searching.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    @cached_property
    def titles_file(self):
        return os.path.join(self.cachedir, 'anime-titles.xml')

    @cached_property
    def pickle_file(self):
        return os.path.join(self.cachedir, 'anime-titles.pickle')

    @cached_property
    def titles_tree(self) -> TitlesTree:
        return self.load_tree()

    def load_tree(self) -> TitlesTree:
        # Try to load from pickled file courageously.
        try:
            titles_tree = TitlesTree.load(self.pickle_file)
        except Exception as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return titles_tree
        # Download titles data if we don't have it.
        if not os.path.exists(self.titles_file):
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
        request = TitlesRequest()
        response = request.open()
        titles_tree = response.xml()
        titles_tree.save(self.titles_file)
        return titles_tree

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles_tree.search(query)
