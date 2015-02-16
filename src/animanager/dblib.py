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

from contextlib import contextmanager
import logging

import mysql.connector

_LOGGER = logging.getLogger(__name__)


@contextmanager
def _dbconnect(*args, **kwargs):
    """MySQL connection context manager."""
    try:
        cnx = mysql.connector.connect(*args, **kwargs)
        cur = cnx.cursor()
        yield cur
        cnx.commit()
    finally:
        cur.close()
        cnx.close()


def connect(dbconfig):
    """Connect using a database configuration."""
    # pylint: disable=star-args
    return _dbconnect(**dbconfig)


def insert(dbconfig, table, fields):
    """Insert a map of fields as a database row.

    Args:
        dbconfig: dict of database config kwargs.
        table: database table.
        fields: dict of database fields.

    """
    query = ', '.join('{}=%s'.format(key) for key in fields)
    query = 'INSERT INTO {} SET {}'.format(table, query)
    values = list(fields.values())
    with connect(dbconfig) as cur:
        cur.execute(query, values)


def update_one(dbconfig, table, fields, values):
    """Update one row."""
    update_many(dbconfig, table, fields, [values])


def update_many(dbconfig, table, fields, values):
    """Update many rows.

    Example:

    anime_update_many(dbconfig, ['foo', 'bar'], [
        # id, then field values
        (1, 'foo_value', 'bar_value'),
    ])

    Args:
        dbconfig: dict of database config kwargs.
        table: database table.
        fields: list of database fields.
        values: list of tuples containing values

    """
    query = ', '.join(('{}=%s'.format(field) for field in fields))
    query = 'UPDATE {} SET {} WHERE id=%s'.format(table, query)
    values = [row[1:] + row[0:1] for row in values]
    with connect(dbconfig) as cur:
        # Must be list comprehension since MySQL connector can't use iterators.
        cur.executemany(query, values)


def select(dbconfig, table, fields, where_filter, where_args=tuple()):
    """Do a SELECT query and return a generator."""
    query = 'SELECT {} FROM {} WHERE {}'.format(
        ', '.join(fields), table, where_filter)
    with connect(dbconfig) as cur:
        cur.execute(query, where_args)
        while True:
            row = cur.fetchone()
            if row:
                yield row
            else:
                break
