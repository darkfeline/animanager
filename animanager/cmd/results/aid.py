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

import functools
import re

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


def _set_last_aid(func):
    """Decorator for setting last_aid."""
    @functools.wraps(func)
    def new_func(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        aid = func(self, *args, **kwargs)
        self.last_aid = aid
        return aid
    return new_func


class AIDResultsManager:

    """Class for managing multiple AIDResults.

    AIDResultsManager allows storing AIDResults from different commands or
    domains and provides a universal parse_aid() method which may dynamically
    draw AIDs from any of the AIDResults that it manages.

    """

    # pylint: disable=too-few-public-methods

    def __init__(self, results):
        self.results = dict(results)
        # Set last_aid, so I don't have to handle None/uninitialized case.
        self.last_aid = 8069

    def __getitem__(self, key):
        return self.results[key]

    def __contains__(self, key):
        return key in self.results

    _key_pattern = re.compile(r'^(\w+):(\d+)$')

    @_set_last_aid
    def parse_aid(self, text, default_key):
        """Parse argument text for aid.

        May retrieve the aid from search result tables as necessary.  aresults
        determines which search results to use by default; True means aresults
        is the default.

        The last aid when no aid has been parsed yet is undefined.

        The accepted formats, in order:

        Last AID:                .
        Explicit AID:            aid:12345
        Explicit result number:  key:12
        Default result number:   12

        """

        if default_key not in self:
            raise ResultKeyError(default_key)

        if text == '.':
            return self.last_aid
        elif text.startswith('aid:'):
            return int(text[len('aid:'):])

        if ':' in text:
            match = self._key_pattern.search(text)
            if not match:
                raise InvalidSyntaxError(text)
            key = match.group(1)
            number = match.group(2)
        else:
            key = default_key
            number = text
        try:
            number = int(number)
        except ValueError:
            raise InvalidSyntaxError(number)

        try:
            return self[key].get_aid(number)
        except KeyError:
            raise ResultKeyError(key)
        except IndexError:
            raise ResultNumberError(key, number)


class AIDParseError(Exception):

    """Generic AID parse error."""


class InvalidSyntaxError(ValueError, AIDParseError):

    """Invalid AID syntax."""

    def __init__(self, text):
        self.text = text
        super().__init__('Invalid syntax: {}'.format(text))


class ResultKeyError(KeyError, AIDParseError):

    """Invalid AID result key."""

    def __init__(self, key):
        self.key = key
        super().__init__('Invalid result key {}'.format(key))


class ResultNumberError(IndexError, AIDParseError):

    """Invalid AID result number."""

    def __init__(self, key, number):
        self.key = key
        self.number = number
        super().__init__('Invalid number {} for key {}'.format(
            number, key))
