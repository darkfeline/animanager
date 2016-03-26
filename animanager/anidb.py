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
from typing import Optional

from animanager.api.anidb import anime, titles
from animanager.cache import cached_property

logger = logging.getLogger(__name__)


class AniDB:

    """Provides access to AniDB data, via cache and API."""

    def __init__(self, cachedir):
        self.cache = AnimeCache(cachedir)

    def lookup(self, aid, force=False):
        """Look up given AID.

        Uses cache if available.

        """
        if force or not self.cache.has(aid):
            request = anime.AnimeRequest(aid)
            response = request.open()
            tree = response.xml()
            self.cache.store(tree)
            return tree
        else:
            return self.cache.retrieve(aid)


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
    def titles_tree(self) -> titles.TitlesTree:
        return self.load_tree()

    def load_tree(self) -> titles.TitlesTree:
        # Try to load from pickled file courageously.
        try:
            titles_tree = titles.TitlesTree.load(self.pickle_file)
        except Exception as e:
            logger.warning('Error loading pickled search cache: %s', e)
        else:
            return titles_tree
        # Download titles data if we don't have it.
        if not os.path.exists(self.titles_file):
            titles_tree = self.fetch()
        else:
            titles_tree = titles.TitlesTree.parse(self.titles_file)
        # Dump a pickled file for next time.
        titles_tree.dump(self.pickle_file)
        return titles_tree

    def fetch(self) -> titles.TitlesTree:
        """Fetch fresh titles data from AniDB."""
        try:
            os.unlink(self.pickle_file)
        except OSError:
            pass
        request = titles.TitlesRequest()
        response = request.open()
        titles_tree = response.xml()
        titles_tree.save(self.titles_file)
        return titles_tree

    def search(self, query):
        """Search titles using a compiled RE query."""
        return self.titles_tree.search(query)


class AnimeCache:

    """Provides access to local cache of AniDB data.

    The AniDB cache is simply a directory containing XML files named <AID>.xml.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    def filepath(self, aid):
        """Return the path to the respective cache file."""
        return os.path.join(self.cachedir, '{}.xml'.format(aid))

    def has(self, aid):
        """Return whether entry is in the cache."""
        return os.path.exists(self.filepath(aid))

    def store(self, tree):
        """Store an entry in the cache."""
        tree.write(self.filepath(tree.aid))

    def retrieve(self, aid):
        """Retrieve an entry from the cache."""
        return anime.AnimeTree.parse(self.filepath(aid))
