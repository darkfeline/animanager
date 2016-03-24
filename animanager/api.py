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
import logging
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods
logger = logging.getLogger(__name__)


class Request(ABC):

    """API request abstract class."""

    @abstractmethod
    def open(self):
        """Perform request."""
        logger.debug('Opened request %s', self)


class HTTPRequest(Request):

    """Implements basic HTTP request behavior."""

    @property
    @abstractmethod
    def request_uri(self):
        return ''

    def open(self):
        super().open()
        return urllib.request.urlopen(self.request_uri)


class Response(ABC):

    @abstractmethod
    def content(self):
        return ''


class HTTPResponse(Response):

    """HTTP response.  Handles gzipped content."""

    def __init__(self, response):
        self.response = response

    def content(self):
        content = self.response.read()
        if self.response.getheader('Content-encoding') == 'gzip':
            content = gzip.decompress(content)
        return content.decode()


class XMLResponse(HTTPResponse):

    """Abstract class for XML responses.

    Implement tree_class property in subclasses.

    """

    @property
    @abstractmethod
    def tree_class(self):
        pass

    def xml(self):
        """Return the lookup data as an XMLResponseTree subclass.

        Can raise APIError in case of error.  Errors include being banned or a
        non-existent AID.

        """
        content = self.content()
        # pylint: disable=not-callable
        tree = self.tree_class(ET.ElementTree(ET.fromstring(content)))
        if tree.error:
            raise APIError(tree)
        return tree


class XMLTree:

    """Base class for handling API XML responses.

    Check error property for any errors.

    parse() class method can be used to load the results from an existing XML
    file containing the data.

    write() method can be used to write the XML data to a file.

    """

    @classmethod
    def parse(cls, file):
        """Create instance from an XML data file."""
        return cls(ET.parse(file))

    def __init__(self, tree: ET.ElementTree) -> None:
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
        return False


class APIError(Exception):
    pass
