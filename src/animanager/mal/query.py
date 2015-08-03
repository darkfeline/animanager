# Copyright (C) 2015  Allen Li
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

"""This package provides MAL query functions."""

from collections import namedtuple
from urllib import request
from urllib.parse import urlencode

from .parse import parse


def setup(config):
    """Set up request module with authentication for MAL API."""
    # set up auth
    auth_handler = request.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='MyAnimeList API',
        uri='http://myanimelist.net',
        **config["mal_args"])
    opener = request.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    request.install_opener(opener)


def _ffrequest(url):
    """urlrequest() using Firefox user agent."""
    req = request.Request(
        url,
        headers={'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 ' +
                 'Firefox/24.0'})
    return request.urlopen(req)

_ANIME_SEARCH_URL = "http://myanimelist.net/api/anime/search.xml?"
_ANIME_FIELDS = ('id', 'title', 'episodes', 'type')

AnimeResult = namedtuple('AnimeResult', ['id', 'title', 'episodes', 'type'])


def anime_search(name):
    """Search MAL for anime."""
    response = _ffrequest(_ANIME_SEARCH_URL + urlencode({'q': name}))
    response = response.read().decode()
    tree = parse(response)
    if tree is None:
        raise ResponseError('No results found for {}'.format(name))
    # Make a list of relevant fields for all entries.
    found = [_get_fields(entry, _ANIME_FIELDS)
             for entry in tree.findall('entry')]
    # Make those fields into AnimeResult tuples.
    found = [AnimeResult(int(id), title, int(episodes), type)
             for id, title, episodes, type in found]
    return found


def _subelement_value(element, subelement_tag):
    """Return the text value of the given subelement.

    Example:

    <entry>
      <spam>eggs</spam>
    </entry>

    get_field(element, "spam") returns "eggs".

    """
    return element.find(subelement_tag).text


def _get_fields(entry, field_list):
    """Get entry fields from a list of XML entities."""
    return [_subelement_value(entry, field) for field in field_list]


class ResponseError(Exception):
    """Unexpected MAL response."""
