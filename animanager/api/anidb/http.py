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

from animanager import api


class HTTPAPIRequest(api.HTTPRequest):

    """AniDB HTTP API request abstract class."""

    CLIENT = 'kfanimanager'
    CLIENTVER = 1
    PROTOVER = 1

    def __init__(self, request):
        self.params = {
            'client': self.CLIENT,
            'clientver': self.CLIENTVER,
            'protover': self.PROTOVER,
            'request': request,
        }

    @property
    def request_uri(self):
        return 'http://api.anidb.net:9001/httpapi?' + \
            urllib.parse.urlencode(self.params)


class XMLTree(api.XMLTree):

    @property
    def error(self):
        if self.root.find('error'):
            return api.APIError()
