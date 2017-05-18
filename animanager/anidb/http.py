# Copyright (C) 2016-2017  Allen Li
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

import gzip

from animanager.xml import XMLTree


def check_for_errors(tree: XMLTree):
    """Check AniDB response XML tree for errors."""
    if tree.root.tag == 'error':
        raise APIError(tree.root.text)


def get_content(response: 'HTTPResponse') -> str:
    """Get content from HTTP response.

    Handles gzipped content.
    """
    content = response.read()
    if response.getheader('Content-encoding') == 'gzip':
        content = gzip.decompress(content)
    return content.decode()


class APIError(Exception):
    """AniDB API error."""
