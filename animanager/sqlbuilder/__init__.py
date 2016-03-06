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

from .tokens import Tokens


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
        self.where_expr = None

    def add_column(self, key):
        self.columns.append(key)

    def where(self, where_expr):
        self.where_expr = where_expr

    def tokens(self):
        tokens = Tokens('SELECT')
        tokens += Tokens.comma_join(
            Tokens.quoted(col) for col in self.columns
        )
        tokens += Tokens('FROM')
        tokens += Tokens.quoted(self.table_name)
        if self.where_expr:
            tokens += Tokens('WHERE')
            tokens += self.where_expr.tokens()
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
        tokens += Tokens.comma_join(
            Tokens.quoted(col) for col in self.columns
        ).paren_wrap()
        tokens += Tokens('VALUES')
        tokens += Tokens.comma_join(
            Tokens('?') for col in self.columns
        ).paren_wrap()
        return tokens


class CreateTable(SQLBuilder):

    def __init__(self, table_name):
        self.table_name = table_name
        self.column_defs = []
        self.table_constraints = []

    def add_column(self, column_name, type=None, pk=False):
        tokens = Tokens.quoted(column_name)
        if type:
            tokens += Tokens(type)
        self.column_defs.append(tokens)
        if pk:
            tokens = Tokens('PRIMARY', 'KEY',
                            '(', Tokens.quote(column_name), ')')
            self.table_constraints.append(tokens)

    def tokens(self):
        tokens = Tokens('CREATE', 'TABLE')
        tokens += Tokens.quoted(self.table_name)
        tokens += Tokens.comma_join(
            chain(
                (tokens for tokens in self.column_defs),
                (tokens for tokens in self.table_constraints),
            )
        ).paren_wrap()
        return tokens
