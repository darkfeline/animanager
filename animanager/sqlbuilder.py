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

from itertools import chain

from abc import ABCMeta, abstractmethod


class Tokens:

    """Class for working with tokens.

    Instances of Tokens represent a list of string tokens.

    Tokens can be created using any number of str.

    >>> Tokens('foo').tokens
    ['foo']

    >>> Tokens('foo', 'bar').tokens
    ['foo', 'bar']

    >>> Tokens().tokens
    []

    TypeError will be raised in other cases:

    >>> Tokens(10)
    Traceback (most recent call last):
        ...
    TypeError: Invalid token type for 10

    >>> Tokens('foo', 10)
    Traceback (most recent call last):
        ...
    TypeError: Invalid token type for 10

    The string representation for Tokens instances is the tokens the instance
    represents joined with spaces.

    >>> str(Tokens('foo', 'bar'))
    'foo bar'

    """

    def __init__(self, *tokens):
        for token in tokens:
            self._check_token(token)
        self.tokens = list(tokens)

    def __str__(self):
        return ' '.join(self.tokens)

    @staticmethod
    def quote(token):
        """Quote a SQL token."""
        return '"{}"'.format(token)

    @staticmethod
    def _check_token(token):
        """Check token type."""
        if not isinstance(token, str):
            raise TypeError('Invalid token type for {!r}'.format(token))

    @classmethod
    def comma_join(cls, *tokens_list):
        """Join Tokens with commas.

        Return a Tokens instance that represents the Tokens arguments joined
        with comma tokens.

        >>> Tokens.comma_join(Tokens('col1', 'int'), Tokens('col2')).tokens
        ['col1', 'int', ',', 'col2']

        """
        tokens = chain(
            tokens_list[0].tokens,
            chain.from_iterable([','] + tokens.tokens
                                for tokens in tokens_list[1:]),
        )
        return cls(*tokens)


class SQLBuilder(metaclass=ABCMeta):

    @abstractmethod
    def tokens(self):
        """Return an iterable of tokens for the query."""

    def build(self):
        """Return the query as a string."""
        return join(self.tokens())


class Select(SQLBuilder):

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def tokens(self):
        tokens = ['SELECT']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(quote(col) for col in self.columns)]
        tokens += [')']
        tokens += ['VALUES']
        tokens += ['(']
        tokens += [','.join('?' for col in self.columns)]
        tokens += [')']
        return tokens


class Insert(SQLBuilder):

    """Simple INSERT statement builder."""

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def tokens(self):
        tokens = ['INSERT', 'INTO']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(quote(col) for col in self.columns)]
        tokens += [')']
        tokens += ['VALUES']
        tokens += ['(']
        tokens += [','.join('?' for col in self.columns)]
        tokens += [')']
        return tokens


class CreateTable(SQLBuilder):

    def __init__(self, table_name):
        self.table_name = table_name
        self.column_defs = []
        self.table_constraints = []

    def add_column(self, column_name, type=None, pk=False):
        tokens = [quote(column_name)]
        if type:
            tokens += [type]
        self.column_defs += [join(tokens)]
        if pk:
            tokens = ['PRIMARY', 'KEY', '(', quote(column_name), ')']
            self.table_constraints += [join(tokens)]

    def tokens(self):
        tokens = ['CREATE', 'TABLE']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(col for col in self.column_defs)]
        for constraint in self.table_constraints:
            tokens += [',']
        tokens += [','.join(col for col in self.column_defs)]
        tokens += [')']
        return tokens
