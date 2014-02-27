#!/usr/bin/env python

from xml.etree import ElementTree
import logging

import mysqllib

import info

logger = logging.getLogger(__name__)

stat_map = {
    'completed': 'complete',
    'plan to watch': 'plan to watch',
    'on-hold': 'on hold',
    'dropped': 'dropped',
}


class IDCounter:

    def __init__(self):
        self.counter = 1
        self.map = {}

    def add(self, name):
        assert name not in self.map
        self.map[name] = self.counter
        self.counter += 1


def _get(e, key):
    return e.find(key).text


def anime(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('anime'):
        name = e.find('series_title').text
        ids.add(name)
        x = [ids.map[name], name] + [e.find(x).text for x in (
            'series_type', 'series_episodes', 'series_animedb_id',
        )]
        logger.debug(x)
        yield x


def myanime(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('anime'):
        name = _get(e, 'series_type')
        x = [ids.map[name]] + [_get(e, x).lower() for x in (
            'my_watched_episodes', 'my_status', 'my_start_date',
            'my_finish_date',
        )]
        x[1] = stat_map[x[1]]
        if x[2] == '0000-00-00':
            x[2] = None
        if x[3] == '0000-00-00':
            x[3] = None
        logger.debug(x)
        yield x


def main(config, file):
    logging.basicConfig(level=logging.DEBUG)
    with mysqllib.connect(**info.db_args) as cur:
        ids = IDCounter()
        cur.executemany(' '.join((
            'INSERT INTO anime',
            '(' + ', '.join((
                'id',
                'name',
                'type',
                'ep_total',
                'animedb_id',
            )) + ')',
            'VALUES',
            '(%s, %s, %s, %s, %s)',
        )), anime(ids, file))
        cur.executemany(' '.join((
            'INSERT INTO myanime',
            '(' + ', '.join((
                'id',
                'ep_watched',
                'status',
                'date_started',
                'date_finished',
            )) + ')'
            'VALUES',
            '(%s, %s, %s, %s, %s)',
        )), myanime(ids, file))

if __name__ == '__main__':
    main()
