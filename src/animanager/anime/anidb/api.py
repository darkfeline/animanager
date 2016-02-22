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

"""AniDB API bindings."""

# XXX Document here.

from abc import ABCMeta, abstractmethod
import datetime
import gzip
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from animanager import errors


class APIRequest(metaclass=ABCMeta):

    """API request abstract class."""

    @abstractmethod
    def open(self):
        """Perform request."""


class HTTPRequest(APIRequest):

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

    def open(self):
        return urllib.request.urlopen(self.request_uri)


class LookupRequest(HTTPRequest):

    """Request for looking up anime by AID via AniDB's HTTP API."""

    def __init__(self, aid):
        super().__init__('anime')
        self.params['aid'] = aid

    def open(self):
        response = super().open()
        return LookupResponse(response)


class LookupResponse:

    """Response from LookupRequest."""

    def __init__(self, response):
        self.response = response

    def _response_body(self):
        body = self.response.read()
        if self.response.getheader('Content-encoding') == 'gzip':
            body = gzip.decompress(body)
        return body.decode()

    def tree(self):
        """Return the lookup data as a LookupTree.

        Can raise APIError in case of error.  Errors include being banned or a
        non-existent AID.

        """
        body = self._response_body()
        tree = LookupTree(ET.ElementTree(ET.fromstring(body)))
        if tree.error:
            raise errors.APIError(tree)
        return tree


def _parse_date(str):
    dt = datetime.datetime.strptime(str, '%Y-%m-%d')
    return dt.date()


class LookupTree:

    """Results from a LookupRequest.

    Check error() for any errors.

    parse() class method can be used to load the results from an existing XML
    file containing the data.

    write() method can be used to write the XML data to a file.

    """

    @classmethod
    def parse(cls, file):
        """Create LookupTree from an XML data file."""
        return cls(ET.parse(file))

    def __init__(self, tree):
        """Initialize LookupTree.

        Be careful, tree should be an ElementTree, specifically a
        xml.etree.ElementTree.ElementTree instance.

        """
        if not isinstance(tree, ET.ElementTree):
            raise TypeError('LookupTree must take an ElementTree object.')
        self.tree = tree
        self.root = tree.getroot()

    def write(self, file):
        """Write XML data to a file."""
        self.tree.write(file)

    @property
    def error(self):
        return self.root.find('error')

    @property
    def aid(self):
        return int(self.root.get('id'))

    @property
    def type(self):
        return self.root.find('type').text

    @property
    def episodecount(self):
        return int(self.root.find('episodecount').text)

    @property
    def startdate(self):
        text = self.root.find('startdate').text
        try:
            return _parse_date(text)
        except ValueError:
            return None

    @property
    def enddate(self):
        text = self.root.find('enddate').text
        try:
            return _parse_date(text)
        except ValueError:
            return None

    @property
    def title(self):
        for element in self.root.find('titles'):
            if element.get('type') == 'main':
                return element.text

    @property
    def episodes(self):
        for element in self.root.find('episodes'):
            yield Episode(element)


class Episode:

    _EPNO_PREFIX = re.compile(r'^[SCPTO]?')

    def __init__(self, element):
        self.element = element

    @property
    def number(self):
        epno = self.element.find('epno').text
        epno = self._EPNO_PREFIX.sub('', epno)
        return int(epno)

    @property
    def type(self):
        return int(self.element.find('epno').get('type'))

    @property
    def length(self):
        return int(self.element.find('length').text)

    @property
    def title(self):
        for title in self.element.iterfind('title'):
            if title.get('xml:lang') == 'ja':
                return title.text
        # In case there's no Japanese title.
        return self.element.find('title').text
