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

from .cache import AniDBCache
from . import api


class AniDB:

    """Provides access to AniDB data, via cache and API."""

    def __init__(self, config):
        self.cache = AniDBCache.from_config(config)

    def lookup(self, aid):
        """Look up given AID.

        Uses cache if available.

        """
        if self.cache.has(aid):
            return self.cache.retrieve(aid)
        else:
            request = api.LookupRequest(aid)
            response = request.open()
            return response.tree()
