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

    __slots__ = ['_tokens']

    def __init__(self, *tokens):
        for token in tokens:
            if not isinstance(token, str):
                raise TypeError('Invalid token type for {}'.format(token))
        self._tokens = tuple(tokens)

    def __str__(self):
        return ' '.join(self._tokens)

    def __repr__(self):
        return 'Tokens({})'.format(
            ', '.join(repr(token) for token in self._tokens)
        )

    def __add__(self, other):
        self._assert_tokens(other)
        tokens = self._tokens + other._tokens
        return Tokens(*tokens)

    @staticmethod
    def _assert_tokens(tokens):
        if not isinstance(tokens, Tokens):
            raise TypeError('Not a Tokens instance: {}'.format(tokens))

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
    def comma_join(cls, tokens_list):
        """Join Tokens with commas.

        Return a Tokens instance that represents the Tokens in tokens_list
        joined with comma tokens.  tokens_list is an iterable.

        >>> Tokens.comma_join([Tokens('col1', 'int'), Tokens('col2')]).tokens
        ['col1', 'int', ',', 'col2']

        >>> Tokens.comma_join([]).tokens
        []

        """
        # We store the iterable's results so we can iterate multiple times.
        tokens_list = list(tokens_list)
        for tokens in tokens_list:
            cls._assert_tokens(tokens)
        if not tokens_list:
            return cls()
        tokens = chain(
            tokens_list[0]._tokens,
            chain.from_iterable([','] + tokens.tokens  # Use a list here.
                                for tokens in tokens_list[1:]),
        )
        tokens = list(tokens)
        return cls(*tokens)

    @property
    def tokens(self):
        return list(self._tokens)

    def paren_wrap(self):
        """Wrap Tokens with parentheses.

        Returns a new Tokens instance without modifying the original.

        >>> Tokens('foo', 'bar').paren_wrap().tokens
        ['(', 'foo', 'bar', ')']

        """
        return Tokens('(', *self._tokens, ')',)
