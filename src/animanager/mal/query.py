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

from . import xmllib


def setup(config):
    """Set up request MAL authentication."""
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

_A_SEARCH = "http://myanimelist.net/api/anime/search.xml?"
_A_SEARCH_FIELDS = ('id', 'title', 'episodes', 'type')
AnimeResult = namedtuple('AnimeResult', ['id', 'title', 'episodes', 'type'])


def anime_search(name):
    """Search MAL for anime."""
    response = _ffrequest(_A_SEARCH + urlencode({'q': name}))
    response = response.read().decode()
    tree = xmllib.parse(response)
    if tree is None:
        raise ResponseError('No results found for %r', name)
    found = [xmllib.get_fields(entity, _A_SEARCH_FIELDS)
             for entity in list(tree)]
    found = [AnimeResult(int(id_), title, int(episodes), type_)
             for id_, title, episodes, type_ in found]
    return found


class ResponseError(Exception):
    """Unexpected MAL response."""
