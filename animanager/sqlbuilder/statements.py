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

from abc import ABCMeta

from .base import SQLBuilder
from .errors import IncompleteQueryError
from .tokens import Tokens
from .expr import BaseExpr
from .expr import Identifier

__all__ = ['Select', 'Insert', 'CreateTable']


class BuilderWithTable(SQLBuilder, metaclass=ABCMeta):

    """Abstract class for SQLBuilder subclasses that work on a table."""

    def __init__(self, table_name):
        self.table = Identifier(table_name)


class Select(BuilderWithTable):

    def __init__(self, table_name):
        super().__init__(table_name)
        self.columns = []
        self.where_expr = None

    def add_column(self, key):
        self.columns.append(Identifier(key))

    def where(self, where_expr):
        if not isinstance(where_expr, BaseExpr):
            raise TypeError('where_expr must be a BaseExpr')
        self.where_expr = where_expr

    def tokens(self):
        tokens = Tokens('SELECT')
        tokens += Tokens.comma_join(
            col.tokens() for col in self.columns
        )
        tokens += Tokens('FROM')
        tokens += self.table.tokens()
        if self.where_expr:
            tokens += Tokens('WHERE')
            tokens += self.where_expr.tokens()
        return tokens

    def build(self):
        if not self.columns:
            raise IncompleteQueryError('must add at least one column')
        return super().build()


class Insert(BuilderWithTable):

    """Simple INSERT statement builder."""

    def __init__(self, table_name):
        super().__init__(table_name)
        self.columns = []

    def add_column(self, column_name):
        self.columns.append(Identifier(column_name))

    def tokens(self):
        tokens = Tokens('INSERT', 'INTO')
        tokens += self.table.tokens()
        tokens += Tokens.comma_join(
            col.tokens() for col in self.columns
        ).paren_wrap()
        tokens += Tokens('VALUES')
        tokens += Tokens.comma_join(
            Tokens('?') for col in self.columns
        ).paren_wrap()
        return tokens

    def build(self):
        if not self.columns:
            raise IncompleteQueryError('must add at least one column')
        return super().build()


class CreateTable(BuilderWithTable):

    def __init__(self, table_name):
        super().__init__(table_name)
        self.column_defs = []
        self.pk = self.PrimaryKey()

    class Column(SQLBuilder):

        def __init__(self, column_name, type=None):
            if type is not None and not isinstance(type, str):
                raise TypeError('type must be a string')
            self.column = Identifier(column_name)
            self.type = type

        def tokens(self):
            tokens = self.column.tokens()
            if self.type:
                tokens += Tokens(self.type)
            return tokens

    class Constraint(SQLBuilder, metaclass=ABCMeta):
        pass

    class PrimaryKey(Constraint):

        def __init__(self):
            self.columns = []

        def __bool__(self):
            return bool(self.columns)

        def add_column(self, column_name):
            if not isinstance(column_name, str):
                raise TypeError('column_name must be a string')
            self.columns.append(Identifier(column_name))

        def tokens(self):
            tokens = Tokens('PRIMARY KEY')
            tokens += Tokens.comma_join(col.tokens() for col in self.columns)
            return tokens

        def build(self):
            if not self.columns:
                raise IncompleteQueryError('must add at least one column')
            return super().build()

    def add_column(self, column_name, type=None, pk=False):
        self.column_defs.append(self.Column(column_name, type))
        if pk:
            self.pk.add_column(column_name)

    def tokens(self):
        tokens = Tokens('CREATE', 'TABLE')
        tokens += Tokens.quoted(self.table_name)
        table_spec = [col.tokens() for col in self.column_defs]
        if self.pk:
            table_spec.append(self.pk.tokens())
        tokens += Tokens.comma_join(table_spec).paren_wrap()
        return tokens

    def build(self):
        if not self.column_defs:
            raise IncompleteQueryError('must add at least one column')
        return super().build()
