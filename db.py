#!/usr/bin/env python3

import pymysql


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
        self.conn.close()


class AnimeDB(Database):

    fields = ('series', 'last_watched', 'total', 'done', 'type', 'season',
              'rating', 'airing_days', 'ep_notes', 'notes')
    field_map = {
        'series': "series=N%(series)s",
        'last_watched': 'last_watched=%(last_watched)s"',
        'total': 'total=%(total)s"',
        'done': 'done=%(done)s"',
        'type': "type=N%(type)s",
        'season': "season=N%(season)s",
        'rating': 'rating=%(rating)s"',
        'airing_days': "airing_days=N%(airing_days)s",
        'ep_notes': "ep_notes=N%(ep_notes)s",
        'notes': "notes=N%(notes)s"}

    def __init__(self):
        super().__init__(user='anime', db='anime', charset='utf8')

    def get(self, key):
        """Get single entry by key

        :param key: search key
        :type key: string
        :rtype: None or tuple

        """
        entries = self.execute("SELECT * FROM anime WHERE series=N%s", key)
        if len(entries) < 1:
            return None
        else:
            return entries[0]

    def search(self, key):
        """Get matches by regex search

        :param key: search key
        :type key: string

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
        query = 'INSERT INTO anime ({}) VALUES({})'.format(
                ','.join(keys),
                ','.join('%({})s'.format(key) for key in keys))
        self.execute(query, entry)

    def change(self, key, map):
        map = map.copy()  # we change map later
        query = "UPDATE anime SET {} WHERE series=N%(key)s".format(
                ','.join(self.field_map[key] for key in map.keys()))
        map['key'] = key
        self.execute(query, map)
