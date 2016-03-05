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

from datetime import date
import logging
import re
import sqlite3

from animanager import errors
from animanager import sqlbuilder

logger = logging.getLogger(__name__)

FIELDS = ['id', 'name', 'type', 'ep_watched', 'ep_total', 'status',
          'date_started', 'date_finished', 'animedb_id']


class AnimeDB:

    """Our anime database."""

    VERSION = 1

    def __init__(self, path):
        self.dbfile = path
        self.connect()
        self._episode_types = None
        self.cache = self.CacheDB()

    def connect(self):
        self.cnx = sqlite3.connect(self.dbfile)
        cur = self.cnx.execute('PRAGMA user_version')
        version = cur.fetchone()[0]
        if version != self.VERSION:
            raise errors.DatabaseVersionError(self.VERSION, version)
        self.cnx.execute('PRAGMA foreign_keys = ON')
        cur = self.cnx.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            raise errors.DBError('Foreign keys are not supported.')

    def close(self):
        self.cnx.close()

    class CacheDB:

        def __init__(self):
            self.cnx = sqlite3.connect(':memory:')

    @property
    def episode_types(self):
        if self._episode_types:
            return self._episode_types
        self._episode_types = dict()
        cur = self.cnx.execute('SELECT id, value, prefix FROM episode_tupe')
        for id, value, prefix in cur:
            self._episode_types[value] = (id, prefix)
        return self._episode_types

    def add(self, anime):
        """Add an anime.

        anime is an AnimeTree containing the necessary information.

        """
        query = sqlbuilder.Insert('anime')
        for col in ('aid', 'title', 'type', 'episodes', 'startdate',
                    'enddate'):
            query.add_column(col)
        self.cnx.execute(
            query.build(),
            (anime.aid, anime.title, anime.type, anime.episodecount,
             anime.startdate, anime.enddate),
        )
        query = sqlbuilder.Insert('episode')
        for col in ('anime', 'type', 'number', 'title', 'length',
                    'user_watched'):
            query.add_column(col)
        for episode in anime.episodes:
            self.cnx.execute(
                query.build(),
                (anime.aid, episode.type, episode.number, episode.title,
                 episode.length, 0),
            )
        self.cnx.commit()

    class WatchingAnime:

        __slots__ = ['aid', 'regexp']

        def __init__(self, aid, regexp):
            self.aid = aid
            self.regexp = re.compile(self.regexp, re.I)

    def get_watching(self):
        """Return watching series."""
        cur = self.cnx.execute('SELECT aid, regexp FROM watching')
        return [self.WatchingAnime(aid, regexp)
                for aid, regexp in cur.fetchall()]


# XXX old
class Database:

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

        # Calculate what needs updating, putting it into a dictionary that we
        # will update at the end all at once.
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

        # Finally, if the series is now complete, we set the status and finish
        # date accordingly.
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
