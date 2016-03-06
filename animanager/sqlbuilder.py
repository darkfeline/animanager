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

    Tokens instances can be concatenated

    >>> Tokens('foo') + Tokens('bar')
    Tokens('foo', 'bar')

    """

    def __init__(self, *tokens):
        for token in tokens:
            if not isinstance(token, str):
                raise TypeError('Invalid token type for {}'.format(token))
        self.tokens = list(tokens)

    def __str__(self):
        return ' '.join(self.tokens)

    def __repr__(self):
        return 'Tokens({})'.format(
            ', '.join(repr(token) for token in self.tokens)
        )

    def __add__(self, other):
        if not isinstance(other, Tokens):
                raise TypeError('Cannot add with {}'.format(other))
        tokens = self.tokens + other.tokens
        return Tokens(*tokens)

    @staticmethod
    def quote(token):
        """Quote a SQL token.

        >>> Tokens.quote('foo')
        '"foo"'

        """
        return '"{}"'.format(token)

    @classmethod
    def quoted(cls, token):
        """Create a Tokens with a quoted token.

        >>> Tokens.quoted('foo')
        Tokens('"foo"')

        """
        return cls(cls.quote(token))

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

    @classmethod
    def paren_wrap(cls, *tokens_list):
        """Wrap Tokens with parentheses.

        >>> Tokens.paren_wrap(Tokens('foo'), Tokens('bar')).tokens
        ['(', 'foo', 'bar', ')']

        """
        return cls(
            '(',
            *chain.from_iterable(tokens.tokens for tokens in tokens_list),
            ')')


class SQLBuilder(metaclass=ABCMeta):

    @abstractmethod
    def tokens(self):
        """Return a Tokens for the current query."""

    def build(self):
        """Return the query as a string."""
        return str(self.tokens())


class Select(SQLBuilder):

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def tokens(self):
        tokens = Tokens('SELECT')
        tokens += Tokens.quoted(self.table_name)
        tokens += Tokens.paren_wrap(
            Tokens.comma_join(
                Tokens.quoted(col) for col in self.columns
            )
        )
        tokens += Tokens('VALUES')
        tokens += Tokens.paren_wrap(
            Tokens.comma_join(
                '?' for col in self.columns
            )
        )
        return tokens


class Insert(SQLBuilder):

    """Simple INSERT statement builder."""

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def tokens(self):
        tokens = Tokens('INSERT', 'INTO')
        tokens += Tokens.quoted(self.table_name)
        tokens += Tokens.paren_wrap(
            Tokens.comma_join(
                Tokens.quoted(col) for col in self.columns
            )
        )
        tokens += Tokens('VALUES')
        tokens += Tokens.paren_wrap(
            Tokens.comma_join(
                '?' for col in self.columns
            )
        )
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
