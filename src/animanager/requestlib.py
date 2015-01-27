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

from urllib import request


def setup(config):
    # set up auth
    auth_handler = request.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='MyAnimeList API',
        uri='http://myanimelist.net',
        **config["mal_args"])
    opener = request.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    request.install_opener(opener)


def ffrequest(url):
    req = request.Request(
        url,
        headers={'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 ' +
                 'Firefox/24.0'})
    return request.urlopen(req)
