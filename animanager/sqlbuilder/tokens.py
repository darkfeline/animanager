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
from functools import reduce
import operator


class Tokens:

    """Class for working with tokens.

    Instances of Tokens represent a list of string tokens.

    Tokens can be created using any number of arguments:

    >>> Tokens('foo')
    Tokens('foo')

    >>> Tokens('foo', 'bar')
    Tokens('foo', 'bar')

    >>> Tokens()
    Tokens()

    TypeError will be raised if non-strings are passed:

    >>> Tokens(9)
    Traceback (most recent call last):
        ...
    TypeError: tokens must be strings

    The string representation for Tokens instances is the tokens the instance
    represents joined with spaces:

    >>> str(Tokens('foo', 'bar'))
    'foo bar'

    Tokens can be accessed as a list of strings via the tokens property:

    >>> Tokens('foo', 'bar')
    ['foo', 'bar']

    Tokens instances can be concatenated:

    >>> Tokens('foo') + Tokens('bar')
    Tokens('foo', 'bar')

    Tokens instances can only be added with other Tokens instances:

    >>> Tokens('foo') + 9
    Traceback (most recent call last):
        ...
    TypeError: can only add with Tokens instances

    """

    __slots__ = ['_tokens']

    def __init__(self, *tokens):
        for token in tokens:
            if not isinstance(token, str):
                raise TypeError('tokens must be strings')
        self._tokens = tuple(tokens)

    def __str__(self):
        return ' '.join(self._tokens)

    def __repr__(self):
        return 'Tokens({})'.format(
            ', '.join(repr(token) for token in self._tokens)
        )

    def __add__(self, other):
        if not isinstance(other, Tokens):
            raise TypeError('can only add with Tokens instances')
        tokens = self._tokens + other._tokens
        return Tokens(*tokens)

    @classmethod
    def join(cls, tokens_list):
        """Join Tokens.

        >>> Tokens.join([Tokens('foo'), Tokens('bar')])
        Tokens('foo', 'bar')

        """
        return reduce(operator.add, tokens_list)

    @classmethod
    def comma_join(cls, tokens_list):
        """Join Tokens with commas.

        Return a Tokens instance that represents the Tokens in tokens_list
        joined with comma tokens.  tokens_list is an iterable.

        >>> Tokens.comma_join([Tokens('col1', 'INTEGER'), Tokens('col2')])
        Tokens('col1', 'INTEGER', ',', 'col2')

        >>> Tokens.comma_join([])
        Tokens()

        """
        # We store the iterable's results so we can iterate multiple times.
        tokens_list = list(tokens_list)
        for tokens in tokens_list:
            if not isinstance(tokens, Tokens):
                raise TypeError(
                    'tokens_list must contain only Tokens instances')
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
        """Return a list of token strings."""
        return list(self._tokens)

    def paren_wrap(self):
        """Wrap Tokens with parentheses.

        Returns a new Tokens instance without modifying the original.

        >>> Tokens('foo', 'bar').paren_wrap()
        Tokens('(', 'foo', 'bar', ')')

        """
        return Tokens('(', *self._tokens, ')',)
