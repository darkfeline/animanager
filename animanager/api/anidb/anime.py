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

"""AniDB HTTP anime API."""

import datetime
import re
from typing import Iterable, Optional

from animanager.api.http import get_content
from animanager.date import parse_date
from animanager.xml import XMLTree

from .http import api_request
from .xml import check_for_errors


def request_anime(aid: int) -> 'AnimeTree':
    """Make an anime API request."""
    response = api_request('anime', aid=aid)
    content = get_content(response)
    tree = AnimeTree.fromstring(content)
    check_for_errors(tree)
    return tree


class AnimeTree(XMLTree):

    """XMLTree repesentation of an anime."""

    @property
    def aid(self) -> int:
        """AniDB ID (AID)."""
        return int(self.root.get('id'))

    @property
    def type(self) -> str:
        """Anime type."""
        return self.root.find('type').text

    @property
    def episodecount(self) -> int:
        """Number of episodes."""
        return int(self.root.find('episodecount').text)

    @property
    def startdate(self) -> Optional[datetime.date]:
        """Start date of anime."""
        text = self.root.find('startdate').text
        try:
            return parse_date(text)
        except ValueError:
            return None

    @property
    def enddate(self) -> Optional[datetime.date]:
        """End date of anime."""
        text = self.root.find('enddate').text
        try:
            return parse_date(text)
        except ValueError:
            return None

    @property
    def title(self) -> str:
        """Main title."""
        for element in self.root.find('titles'):
            if element.get('type') == 'main':
                return element.text

    @property
    def episodes(self) -> Iterable['Episode']:
        """The anime's episodes."""
        for element in self.root.find('episodes'):
            yield Episode(element)


class Episode:

    """Episode XML element."""

    _NUMBER_SUFFIX = re.compile(r'(\d+)$')

    def __init__(self, element):
        self.element = element

    @property
    def epno(self) -> str:
        """Concatenation of type and episode number.

        Unique for an anime.

        """
        return self.element.find('epno').text

    @property
    def number(self) -> int:
        """Episode number.

        Unique for an anime and episode type, but not unique across episode
        types for the same anime.

        """
        epno = self.element.find('epno').text
        match = self._NUMBER_SUFFIX.search(epno)
        return int(match.group(1))

    @property
    def type(self) -> int:
        """Episode type."""
        return int(self.element.find('epno').get('type'))

    @property
    def length(self) -> int:
        """Length of episode in minutes."""
        return int(self.element.find('length').text)

    @property
    def title(self) -> str:
        """Episode title."""
        for title in self.element.iterfind('title'):
            if title.get('xml:lang') == 'ja':
                return title.text
        # In case there's no Japanese title.
        return self.element.find('title').text
