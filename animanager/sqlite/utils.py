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

"""SQLite utilities."""


def _sqlpformat(name):
    return '{0}=:{0}'.format(name)


def upsert(db, table, key_cols, update_dict):
    """Fabled upsert for SQLiteDB.

    Perform an upsert based on primary key.

    :param SQLiteDB db: database
    :param str table: table to upsert into
    :param str key_cols: name of key columns
    :param dict update_dict: key-value pairs to upsert

    """
    with db:
        cur = db.cursor()
        cur.execute(
            'UPDATE {} SET {} WHERE {}'.format(
                table,
                ','.join(_sqlpformat(col) for col in update_dict.keys()),
                ' AND '.join(_sqlpformat(col) for col in key_cols),
            ),
            update_dict,
        )
        if db.changes() == 0:
            keys, values = zip(*update_dict.items())
            cur.execute(
                'INSERT INTO {} ({}) VALUES ({})'.format(
                    table,
                    ','.join(keys),
                    ','.join('?' for _ in values)),
                values)
