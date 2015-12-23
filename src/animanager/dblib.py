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

from datetime import date
import logging
import sqlite3
import sys

_LOGGER = logging.getLogger(__name__)

FIELDS = ['id', 'name', 'type', 'ep_watched', 'ep_total', 'status',
          'date_started', 'date_finished', 'animedb_id']


class Database:

    def __init__(self, path):
        self.dbfile = path
        self._connect()

    def _connect(self):
        self.cnx = sqlite3.connect(self.dbfile)
        cur = self.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            _LOGGER.critical('Foreign keys are not supported.')
            sys.exit(1)

    @classmethod
    def from_config(cls, config):
        return cls(config['general'].getpath('database'))

    def cursor(self):
        return self.cnx.cursor()

    def commit(self):
        self.cnx.commit()

    def close(self):
        self.cnx.close()

    def bump(self, id):
        """Bump a series.

        Increment the episodes watched count of one series, and do all of the
        housekeeping that it entails.

        """
        results = self.select(
            table='anime',
            fields=['ep_watched', 'ep_total', 'status'],
            where_filter='id=?',
            where_args=(id,)
        )
        watched, total, status = next(results)

        # Calculate what needs updating, putting it into a dictionary that we will
        # update at the end all at once.
        update_map = dict()

        # We set the starting date if we haven't watched anything yet.
        if watched == 0:
            update_map['date_started'] = date.today().isoformat()

        # We update the episode count.
        watched += 1
        update_map['ep_watched'] = watched

        # If the status wasn't watching, we set it so.
        if status != 'watching':
            update_map['status'] = 'watching'

        # Finally, if the series is now complete, we set the status and finish date
        # accordingly.
        if watched == total and total is not None:
            update_map['status'] = 'complete'
            update_map['date_finished'] = date.today().isoformat()

        # Now we update all of the changes we have gathered.
        self.update_one('anime', id, update_map)

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
