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

"""AID-specific results handling."""

import re

from .errors import (
    InvalidResultKeyError, InvalidResultNumberError, InvalidSyntaxError,
)
from .results import Results

__all__ = ['AIDResults', 'AIDResultsManager']


class AIDResults(Results):

    """SearchResults subclass that guarantees the presence of an aid column."""

    def __init__(self, headers, results=()):
        super().__init__(['AID'] + headers, results)

    def __repr__(self):
        return 'AIDResults({}, {})'.format(
            self.headers[2:],
            self.results,
        )

    def get_aid(self, number):
        """Get the AID of the given result row number."""
        return self.get(number)[0]


class AIDResultsManager:

    """Class for managing multiple AIDResults.

    AIDResultsManager allows storing AIDResults from different commands or
    domains and provides a universal parse_aid() method which may dynamically
    draw AIDs from any of the AIDResults that it manages.

    """

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

        if default_key not in self:
            raise InvalidResultKeyError(default_key)

        if text.startswith('aid:'):
            return int(text[len('aid:'):])
        elif text.startswith('#'):
            match = self._key_pattern.match(text)
            if not match:
                raise InvalidSyntaxError(text)
            key, number = match.groups()
            number = int(number)
        else:
            key = default_key
            try:
                number = int(text)
            except ValueError:
                raise InvalidSyntaxError(text)

        try:
            return self[key].get_aid(number)
        except KeyError:
            raise InvalidResultKeyError(key)
        except IndexError:
            raise InvalidResultNumberError(key, number)
