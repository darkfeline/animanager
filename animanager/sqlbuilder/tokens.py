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

    The string representation for Tokens instances is a query string that
    tokenizes to the same tokens.  The current implementation merely joins the
    tokens with spaces.  This behavior is part of the interface and can be
    relied upon.

    >>> str(Tokens('foo', 'bar'))
    'foo bar'

    Tokens instances are also iterables and yield their token strings.

    >>> for x in Tokens('foo', 'bar'):
    ...     print(repr(x))
    'foo'
    'bar'

    Tokens instances can be concatenated:

    >>> Tokens('foo') + Tokens('bar')
    Tokens('foo', 'bar')

    Tokens instances can only be added with other Tokens instances:

    >>> Tokens('foo') + 9
    Traceback (most recent call last):
        ...
    TypeError: can only add with Tokens instances

    """

    __slots__ = ['tokens']

    def __init__(self, *tokens):
        for token in tokens:
            if not isinstance(token, str):
                raise TypeError('tokens must be strings')
        self.tokens = tuple(tokens)

    def __str__(self):
        return ' '.join(self.tokens)

    def __repr__(self):
        return 'Tokens({})'.format(
            ', '.join(repr(token) for token in self.tokens)
        )

    def __add__(self, other):
        if not isinstance(other, Tokens):
            raise TypeError('can only add with Tokens instances')
        tokens = self.tokens + other.tokens
        return Tokens(*tokens)

    def __iter__(self):
        return iter(self.tokens)

    def join(self, tokens_list):
        """Join Tokens instances with self.

        This works like str.join().

        >>> Tokens().join([Tokens('foo'), Tokens('bar')])
        Tokens('foo', 'bar')

        >>> Tokens(',').join([Tokens('col1', 'INTEGER'), Tokens('col2')])
        Tokens('col1', 'INTEGER', ',', 'col2')

        >>> Tokens(',').join([])
        Tokens()

        This is more efficient than concatenating many Tokens, since
        concatenation creates a new Tokens instance at each step, while join()
        only creates one new Tokens instance.

        """

        # We store the iterable's results so we can iterate multiple times.
        tokens_list = list(tokens_list)
        if not tokens_list:
            return Tokens()
        for tokens in tokens_list:
            if not isinstance(tokens, Tokens):
                raise TypeError(
                    'tokens_list must contain only Tokens instances')
        joined_tokens = list(tokens_list[0].tokens)
        for tokens in tokens_list[1:]:
            joined_tokens.extend(self.tokens)
            joined_tokens.extend(tokens.tokens)
        return Tokens(*joined_tokens)

    def paren_wrap(self):
        """Wrap Tokens with parentheses.

        Returns a new Tokens instance without modifying the original.

        >>> Tokens('foo', 'bar').paren_wrap()
        Tokens('(', 'foo', 'bar', ')')

        """
        return Tokens('(', *self.tokens, ')',)
