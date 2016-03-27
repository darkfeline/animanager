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

"""Generic results handling."""

from tabulate import tabulate

__all__ = ['Results']


class Results:

    """Class for managing command results for subsequent commands to access.

    >>> Results(['title'])
    Results(['title'], [])

    You can pass initial results:

    >>> Results(['title'], [('Konosuba',), ('Oreimo',)])
    Results(['title'], [('Konosuba',), ('Oreimo',)])

    """

    def __init__(self, headers, results=()):
        self.table_width = len(headers)
        self.headers = ['#'] + headers
        self.set(results)

    def __repr__(self):
        return 'Results({}, {})'.format(
            self.headers[1:],
            self.results
        )

    def append(self, row):
        """Append a result row and check its length.

        >>> x = Results(['title', 'type'])
        >>> x.append(('Konosuba', 'TV'))
        >>> x
        Results(['title', 'type'], [('Konosuba', 'TV')])

        >>> x.append(('Konosuba',))
        Traceback (most recent call last):
            ...
        ValueError: Wrong result row length

        """
        row = tuple(row)
        if len(row) != self.table_width:
            raise ValueError('Wrong result row length')
        self.results.append(row)

    def set(self, results):
        """Set results.

        results is an iterable of tuples, where each tuple is a row of results.

        >>> x = Results(['title'])
        >>> x.set([('Konosuba',), ('Oreimo',)])
        >>> x
        Results(['title'], [('Konosuba',), ('Oreimo',)])

        """
        self.results = list()
        for row in results:
            self.append(row)

    def get(self, number):
        """Get a result row.

        results are indexed from 1.

        >>> Results(['title'], [('Konosuba',), ('Oreimo',)]).get(1)
        ('Konosuba',)

        >>> Results(['title'], [('Konosuba',), ('Oreimo',)]).get(3)
        Traceback (most recent call last):
            ...
        IndexError: list index out of range

        """
        return self.results[number - 1]

    def print(self):
        """Print results table.

        >>> Results(['title'], [('Konosuba',), ('Oreimo',)]).print()
          #  title
        ---  --------
          1  Konosuba
          2  Oreimo

        """
        print(tabulate(
            ((i, *row) for i, row in enumerate(self.results, 1)),
            headers=self.headers,
        ))
