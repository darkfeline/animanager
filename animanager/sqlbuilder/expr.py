# Copyright (C) 2015-2016  Allen Li
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

from numbers import Real

from .base import SQLBuilder
from .tokens import Tokens

__all__ = ['BinaryOp', 'Identifier']


class BaseExpr(SQLBuilder):

    """Abstract class for SQLite expr."""


class BinaryOp(BaseExpr):

    """Represents a binary operation."""

    def __init__(self, operator, expr1, expr2):
        if not isinstance(operator, str):
            raise TypeError('operator must be a string')
        if not isinstance(expr1, BaseExpr) or not isinstance(expr2, BaseExpr):
            raise TypeError('exprs must be BaseExpr instances')
        self.operator = operator
        self.expr1 = expr1
        self.expr2 = expr2

    def tokens(self):
        return Tokens().join([
            self.expr1.tokens(),
            Tokens(self.operator),
            self.expr2.tokens()])


class BaseLiteral(BaseExpr):
    pass


class Literal(BaseLiteral):

    """A SQL literal.

    Literal will return the proper subclass for its argument:

    >>> Literal(9)
    NumericLiteral(9)

    >>> Literal('hi')
    TextLiteral('hi')

    >>> Literal(dict())
    Traceback (most recent call last):
        ...
    TypeError: value must be a supported literal type

    """

    def __new__(cls, value):
        if isinstance(value, str):
            return TextLiteral(value)
        elif isinstance(value, Real):
            return NumericLiteral(value)
        else:
            raise TypeError('value must be a supported literal type')


class TextLiteral(BaseLiteral):

    """A SQL text literal.

    >>> TextLiteral('hello world')
    TextLiteral('hello world')

    >>> TextLiteral('hello world').tokens()
    Tokens("'hello world'")

    Single quotes will be escaped:

    >>> TextLiteral("megumin's megumins").tokens()
    Tokens("'megumin''s megumins'")

    text must be a string:

    >>> TextLiteral(9)
    Traceback (most recent call last):
        ...
    TypeError: text must be a string

    """

    def __init__(self, text):
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        self.text = text

    def __repr__(self):
        return 'TextLiteral({!r})'.format(self.text)

    def tokens(self):
        # Escape single quotes for SQL.
        text = self.text.replace("'", "''")
        return Tokens("'{}'".format(text))


class NumericLiteral(BaseLiteral):

    """A SQL numeric literal.

    >>> NumericLiteral(9)
    NumericLiteral(9)

    >>> NumericLiteral(9).tokens()
    Tokens('9')

    numeric must be a Real, that is, any Python non-imaginary numeric type:

    >>> NumericLiteral(1j)
    Traceback (most recent call last):
        ...
    TypeError: numeric must be a Real

    """

    def __init__(self, numeric):
        if not isinstance(numeric, Real):
            raise TypeError('numeric must be a Real')
        self.numeric = numeric

    def __repr__(self):
        return 'NumericLiteral({})'.format(self.numeric)

    def tokens(self):
        return Tokens(str(self.numeric))


class Identifier(BaseExpr):

    """Represents a quoted identifier.

    >>> Identifier('column')
    Identifier('column')

    >>> Identifier('column').tokens()
    Tokens('"column"')

    identifier must be a non-empty string:

    >>> Identifier(9)
    Traceback (most recent call last):
        ...
    TypeError: identifier must be a string

    >>> Identifier('')
    Traceback (most recent call last):
        ...
    TypeError: identifier cannot be empty

    """

    def __init__(self, identifier):
        if not isinstance(identifier, str):
            raise TypeError('identifier must be a string')
        if not identifier:
            raise ValueError('identifier cannot be empty')
        self.identifier = identifier

    def __repr__(self):
        return 'Identifier({!r})'.format(self.identifier)

    def tokens(self):
        return Tokens('"{}"'.format(self.identifier))
