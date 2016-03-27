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

import gzip
import urllib.parse
import urllib.request
from abc import abstractmethod

from .abc import Request, Response


class HTTPRequest(Request):

    """Implements basic HTTP request behavior."""

    @property
    @abstractmethod
    def request_uri(self):
        return ''

    def open(self):
        super().open()
        return urllib.request.urlopen(self.request_uri)


class HTTPResponse(Response):

    """HTTP response.  Handles gzipped content."""

    def __init__(self, response):
        self.response = response

    def content(self):
        content = self.response.read()
        if self.response.getheader('Content-encoding') == 'gzip':
            content = gzip.decompress(content)
        return content.decode()
