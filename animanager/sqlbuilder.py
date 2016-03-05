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

from abc import ABCMeta, abstractmethod


def quote(token):
    """Quote a SQL token."""
    return '"{}"'.format(token)


def join(tokens):
    """Join tokens to make a SQL query."""
    return ' '.join(tokens)


class SQLBuilder(metaclass=ABCMeta):

    @abstractmethod
    def build(self):
        pass


class Insert:

    """Simple INSERT statement builder."""

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def build(self):
        tokens = ['INSERT', 'INTO']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(quote(col) for col in self.columns)]
        tokens += [')']
        tokens += ['VALUES']
        tokens += ['(']
        tokens += [','.join('?' for col in self.columns)]
        tokens += [')']
        return join(tokens)


class CreateTable:

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

    def build(self):
        tokens = ['CREATE', 'TABLE']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(col for col in self.column_defs)]
        for constraint in self.table_constraints:
            tokens += [',']
        tokens += [','.join(col for col in self.column_defs)]
        tokens += [')']
        return join(tokens)
