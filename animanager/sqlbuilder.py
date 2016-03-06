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


def quote(token):
    """Quote a SQL token."""
    return '"{}"'.format(token)


def join(tokens):
    """Join tokens to make a SQL query."""
    return ' '.join(tokens)


def comma_join(tokens):
    """Join tokens with commas.

    Takes a list of tokens and returns a list of those tokens separated with
    comma tokens.

    """
    return list(
        chain([tokens[0]],
              chain.from_iterable([',', token] for token in tokens[1:]))
    )


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
