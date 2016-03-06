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

from .base import SQLBuilder
from .tokens import Tokens

__all__ = ['Identifier']


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


class Identifier(BaseExpr):

    """Represents a quoted identifier.

    >>> Identifier('column').tokens()
    Tokens('"column"')

    """

    def __init__(self, identifier):
        if not isinstance(identifier, str):
            raise TypeError('identifier must be a string')
        if not identifier:
            raise ValueError('identifier cannot be empty')
        self.identifier = identifier

    def tokens(self):
        return Tokens('"{}"'.format(self.identifier))
