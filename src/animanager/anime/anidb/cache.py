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

import os

from .api import LookupTree


class AniDBCache:

    """Provides access to local cache of AniDB data.

    The AniDB cache is simply a directory containing XML files named <AID>.xml.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    @classmethod
    def from_config(cls, config):
        """Create instance from config."""
        return cls(config['anime'].getpath('anidb_cache'))

    def filepath(self, aid):
        """Return the path to the respective cache file."""
        return os.path.join(self.cachedir, '{}.xml'.format(aid))

    def has(self, aid):
        """Return whether entry is in the cache."""
        return os.path.exists(self.filepath(aid))

    def store(self, tree):
        """Store a LookupTree in the cache."""
        tree.write(self.filepath(tree.aid))

    def retrieve(self, aid):
        """Retrieve a LookupTree from the cache."""
        return LookupTree.parse(self.filepath(aid))
