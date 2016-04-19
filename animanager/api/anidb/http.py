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

"""The module contains classes for working with AniDB's HTTP API."""

import urllib.parse
from urllib.request import urlopen

CLIENT = 'kfanimanager'
CLIENTVER = 1
PROTOVER = 1


def api_request(request: str, **params):
    """Make an AniDB HTTP API request."""
    request_params = {
        'client': CLIENT,
        'clientver': CLIENTVER,
        'protover': PROTOVER,
        'request': request,
    }
    request_params.update(params)
    return urlopen(
        'http://api.anidb.net:9001/httpapi?' +
        urllib.parse.urlencode(request_params))
