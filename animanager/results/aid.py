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

import re

import animanager.results


class AIDResults(animanager.results.Results):

    """SearchResults subclass that guarantees the presence of an aid column."""

    def __init__(self, headers, results=()):
        super().__init__(['AID'] + headers, results)

    def __repr__(self):
        return 'AIDSearchResults({}, {})'.format(
            self.headers[2:],
            self.results,
        )

    def get_aid(self, number):
        return self.get(number)[0]


class AIDResultsManager:

    """Class for managing results and AID parsing."""

    def __init__(self):
        self.results = dict()

    def __getitem__(self, key):
        return self.results[key]

    def __setitem__(self, key, value):
        self.results[key] = value

    def __contains__(self, key):
        return key in self.results

    _key_pattern = re.compile(r'#(\w+):(\d+)')

    def parse_aid(self, text, default_key):
        """Parse argument text for aid.

        May retrieve the aid from search result tables as necessary.  aresults
        determines which search results to use by default; True means aresults
        is the default.

        The accepted formats, in order:

        Explicit AID:             aid:12345
        Explicit result number:   #key:12
        Default result number:    12

        """
        if text.startswith('aid:'):
            return int(text[len('aid:'):])
        elif text.startswith('#'):
            match = self._key_pattern.match(text)
            if not match:
                raise ValueError('Invalid aid syntax')
            key, number = match.groups()
            number = int(number)
        else:
            key = default_key
            number = int(text)
        return self[key].get_aid(number)
