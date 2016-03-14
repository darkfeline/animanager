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

from tabulate import tabulate


class SearchResults:

    """Class for managing search results for commands to access.

    >>> SearchResults(['title'])
    SearchResults(['title'], [])

    You can pass initial results:

    >>> SearchResults(['title'], [('Konosuba',), ('Oreimo',)])
    SearchResults(['title'], [('Konosuba',), ('Oreimo',)])

    """

    def __init__(self, headers, results=()):
        self.headers = ['#'] + headers
        self.set(results)

    def __repr__(self):
        return 'SearchResults({}, {})'.format(
            self.headers[1:],
            self.results
        )

    def append(self, row):
        """Append a result row and check its length.

        >>> x = SearchResults(['title', 'type'])
        >>> x.append(('Konosuba', 'TV'))
        >>> x
        SearchResults(['title', 'type'], [('Konosuba', 'TV')])
        >>> x.append(('Konosuba',))
        Traceback (most recent call last):
            ...
        ValueError: Wrong result row length

        """
        row = tuple(row)
        if len(row) != len(self.headers) - 1:
            raise ValueError('Wrong result row length')
        self.results.append(row)

    def set(self, results):
        """Set results.

        results is an iterable of tuples, where each tuple is a row of results.

        >>> x = SearchResults(['title'])
        >>> x.set([('Konosuba',), ('Oreimo',)])
        >>> x
        SearchResults(['title'], [('Konosuba',), ('Oreimo',)])

        """
        self.results = list()
        for row in results:
            self.append(row)

    def get(self, number):
        """Get a result row.

        results are indexed from 1.

        >>> SearchResults(['title'], [('Konosuba',), ('Oreimo',)]).get(1)
        ('Konosuba',)

        """
        return self.results[number - 1]

    def print(self):
        """Print results table."""
        print(tabulate(
            ((i, *row) for i, row in enumerate(self.results, 1)),
            headers=self.headers,
        ))


class AIDSearchResults(SearchResults):

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
