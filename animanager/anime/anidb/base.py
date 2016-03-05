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

from abc import ABCMeta, abstractmethod
import gzip
import logging
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from animanager import errors

logger = logging.getLogger(__name__)


class Request(metaclass=ABCMeta):

    """API request abstract class."""

    @abstractmethod
    def open(self):
        """Perform request."""
        logger.debug('Opened request %s', self)


class HTTPRequest(Request, metaclass=ABCMeta):

    """Implements basic HTTP request behavior."""

    def open(self):
        super().open()
        return urllib.request.urlopen(self.request_uri)


class HTTPAPIRequest(HTTPRequest):

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


class HTTPResponse:

    """HTTP response.  Handles gzipped content."""

    def __init__(self, response):
        self.response = response

    def response_content(self):
        content = self.response.read()
        if self.response.getheader('Content-encoding') == 'gzip':
            content = gzip.decompress(content)
        return content.decode()


class XMLResponse(HTTPResponse, metaclass=ABCMeta):

    """Abstract class for returning XMLResponseTree.

    Define tree_class attribute in implementation subclasses.

    """

    tree_class = None

    def xml(self):
        """Return the lookup data as an XMLResponseTree subclass.

        Can raise APIError in case of error.  Errors include being banned or a
        non-existent AID.

        """
        content = self.response_content()
        tree = self.tree_class(ET.ElementTree(ET.fromstring(content)))
        if tree.error:
            raise errors.APIError(tree)
        return tree


class XMLTree(metaclass=ABCMeta):

    """Abstract class for handling API XML responses.

    Check error() for any errors.

    parse() class method can be used to load the results from an existing XML
    file containing the data.

    write() method can be used to write the XML data to a file.

    """

    @classmethod
    def parse(cls, file):
        """Create instance from an XML data file."""
        return cls(ET.parse(file))

    def __init__(self, tree):
        """Initialize instance.

        Be careful, tree should be an ElementTree, specifically a
        xml.etree.ElementTree.ElementTree instance.

        """
        if not isinstance(tree, ET.ElementTree):
            raise TypeError('Not an ElementTree object.')
        self.tree = tree
        self.root = tree.getroot()

    def write(self, file):
        """Write XML data to a file."""
        self.tree.write(file)

    @property
    def error(self):
        return self.root.find('error')
