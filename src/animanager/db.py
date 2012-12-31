#!/usr/bin/env python3

import logging

import pymysql

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(*args, **kwargs)

    def execute(self, cmd, args=None):
        """
        :param cmd: MySQL query
        :type cmd: str
        :param args: string substition param used by pymysql

        """
        cur = self.conn.cursor()
        cur.execute(cmd, args)
        return cur.fetchall()
        cur.close()

    def close(self):
        self.conn.commit()
        self.conn.close()


class AnimeDB(Database):

    fields = ('series', 'last_watched', 'total', 'done', 'type', 'season',
              'rating', 'airing_days', 'ep_notes', 'notes')
    field_map = {
        'series': 'series=N%(series)s',
        'last_watched': 'last_watched=%(last_watched)s',
        'total': 'total=%(total)s',
        'done': 'done=%(done)s',
        'type': 'type=N%(type)s',
        'season': 'season=N%(season)s',
        'rating': 'rating=%(rating)s',
        'airing_days': 'airing_days=N%(airing_days)s',
        'ep_notes': 'ep_notes=N%(ep_notes)s',
        'notes': 'notes=N%(notes)s'}

    def __init__(self):
        super().__init__(
            unix_socket='/run/mysqld/mysqld.sock', user='anime', db='anime',
            charset='utf8')

    def get(self, key):
        """
        Get single entry by key

        :param key: key
        :type key: str
        :rtype: None or tuple

        """
        entries = self.execute("SELECT * FROM anime WHERE series=N%s", key)
        if len(entries) < 1:
            return None
        else:
            return entries[0]

    def search(self, key):
        """
        Get matches by regex search

        :param key: search key
        :type key: str

        """
        entries = self.execute(
            "SELECT * FROM anime WHERE series REGEXP N%s", r'.*' + key + r'.*')
        return entries

    def add(self, entry):
        """
        :param entry: entry
        :type entry: dict

        """
        keys = list(entry.keys())
        assert 'series' in keys
        query = 'INSERT INTO anime ({}) VALUES({})'.format(
                ','.join(keys),
                ','.join('%({})s'.format(key) for key in keys))
        self.execute(query, entry)

    def delete(self, key):
        """
        Delete entry with given key

        :param key: key
        :type key: str

        """
        self.execute("DELETE FROM anime WHERE series=N%s", key)

    def change(self, key, map):
        """
        Change an entry

        :param key: key
        :type key: str
        :param map: values
        :type map: dict

        """
        map = map.copy()  # we change map later
        query = "UPDATE anime SET {} WHERE series=N%(key)s".format(
                ','.join(self.field_map[key] for key in map.keys()))
        map['key'] = key
        logger.debug('Query:{}'.format(query))
        logger.debug('Map:{}'.format(map))
        self.execute(query, map)
