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


class SQLBuilder(metaclass=ABCMeta):

    @staticmethod
    def quote(token):
        return '"{}"'.format(token)

    @abstractmethod
    def build(self):
        pass


class Insert:

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def add_column(self, key):
        self.columns.append(key)

    def build(self):
        tokens = []
        tokens += ['INSERT', 'INTO']
        tokens += [self.quote(self.table_name)]
        tokens += ['(']
        tokens += [','.join(self.quote(col) for col in self.columns)]
        tokens += [')']
        tokens += ['VALUES']
        tokens += ['(']
        tokens += [','.join('?' for col in self.columns)]
        tokens += [')']
