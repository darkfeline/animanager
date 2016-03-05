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

import datetime
import os
import re

from . import base


class AnimeRequest(base.HTTPAPIRequest):

    """Request for looking up anime by AID via AniDB's HTTP API."""

    def __init__(self, aid):
        super().__init__('anime')
        self.params['aid'] = aid

    def open(self):
        response = super().open()
        return AnimeResponse(response)


def _parse_date(str):
    """Parse an ISO format date (YYYY-mm-dd)."""
    dt = datetime.datetime.strptime(str, '%Y-%m-%d')
    return dt.date()


class AnimeTree(base.XMLTree):

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


class AnimeResponse(base.XMLResponse):

    """Response from AnimeRequest."""

    tree_class = AnimeTree


class AnimeCache:

    """Provides access to local cache of AniDB data.

    The AniDB cache is simply a directory containing XML files named <AID>.xml.

    """

    def __init__(self, cachedir):
        self.cachedir = cachedir

    def filepath(self, aid):
        """Return the path to the respective cache file."""
        return os.path.join(self.cachedir, '{}.xml'.format(aid))

    def has(self, aid):
        """Return whether entry is in the cache."""
        return os.path.exists(self.filepath(aid))

    def store(self, tree):
        """Store an entry in the cache."""
        tree.write(self.filepath(tree.aid))

    def retrieve(self, aid):
        """Retrieve an entry from the cache."""
        return AnimeTree.parse(self.filepath(aid))
