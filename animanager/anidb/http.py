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

"""The module contains classes for working with AniDB's HTTP API.

.. data:: CLIENT

   AniDB API client name.

.. data:: CLIENTVER

   AniDB API client version.

.. data:: PROTOVER

   AniDB API protocol version.

"""

import gzip
import urllib.parse
from http.client import HTTPResponse
from urllib.request import urlopen

from animanager.xml import XMLTree

CLIENT = 'kfanimanager'
CLIENTVER = 1
PROTOVER = 1


def api_request(request: str, **params):
    """Make an AniDB HTTP API request.

    Check the `AniDB documentation
    <https://wiki.anidb.net/w/HTTP_API_Definition>`_ for details on `request`
    and `params`.

    """
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


def check_for_errors(tree: XMLTree) -> None:
    """Check AniDB response XML tree for errors.

    :raises APIError: error found

    """
    if tree.root.find('error'):
        raise APIError()


def get_content(response: HTTPResponse) -> str:
    """Get content from HTTP response.

    Handles gzipped content.

    :param HTTPResponse response: HTTP response
    :returns: HTTP response content
    :rtype: str

    """
    content = response.read()
    if response.getheader('Content-encoding') == 'gzip':
        content = gzip.decompress(content)
    return content.decode()


class APIError(Exception):
    """AniDB API error."""
