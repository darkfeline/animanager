# Copyright (C) 2015  Allen Li
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

"""Tools for animanager MySQL database."""

import logging
import sqlite3
import os
import sys

_LOGGER = logging.getLogger(__name__)


class Database:

    defaultpath = os.path.join(os.environ['HOME'], '.animanager',
                               'database.db')

    def __init__(self, path=None):
        if path is None:
            self.dbfile_path = self.defaultpath
        else:
            self.dbfile_path = path
        self._connect()

    def _connect(self):
        self.cnx = sqlite3.connect(self.dbfile_path)
        cur = self.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            _LOGGER.critical('Foreign keys are not supported.')
            sys.exit(1)

    def cursor(self):
        return self.cnx.cursor()

    def commit(self):
        self.cnx.commit()

    def close(self):
        self.cnx.close()

    def insert(self, table, fields):
        """Insert a map of fields as a database row.

        Args:
            table: database table.
            fields: dict of database fields.

        """
        keys = list(fields.keys())
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(
            table,
            ', '.join(key for key in keys),
            ', '.join('?' for key in keys),
        )
        values = list(fields[key] for key in keys)
        cur = self.cursor()
        cur.execute(query, values)
        self.commit()
        return cur.lastrowid

    def update_many(self, table, fields, values):
        """Update many rows.

        Example:

        db.update_many(
            ['foo', 'bar'],
            [
                # id, then field values
                (1, 'foo_value', 'bar_value'),
            ]
        )

        Args:
            table: database table.
            fields: list of database fields.
            values: list of tuples containing values

        """
        query = ', '.join(('{}=?'.format(field) for field in fields))
        query = 'UPDATE {} SET {} WHERE id=?'.format(table, query)
        values = [row[1:] + row[0:1] for row in values]
        cur = self.cursor()
        cur.executemany(query, values)
        self.commit()

    def update_one(self, table, id, map):
        """Update one row."""
        keys = list(map.keys())
        self.update_many(table, keys, ([id] + [map[k] for k in keys],))

    def select(self, table, fields, where_filter, where_args=tuple()):
        """Do a SELECT query and return a generator."""
        query = 'SELECT {} FROM {} WHERE {}'.format(
            ', '.join(fields),
            table,
            where_filter,
        )
        cur = self.cursor()
        cur.execute(query, where_args)
        while True:
            row = cur.fetchone()
            if row:
                yield row
            else:
                break
