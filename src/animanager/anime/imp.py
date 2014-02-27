#!/usr/bin/env python

from xml.etree import ElementTree
import logging

from animanager import mysqllib

logger = logging.getLogger(__name__)

stat_map = {
    'watching': 'watching',
    'completed': 'complete',
    'plan to watch': 'plan to watch',
    'on-hold': 'on hold',
    'dropped': 'dropped',
}


class IDCounter:

    def __init__(self):
        self.counter = 1
        self.map = {}

    def add(self, id):
        assert id not in self.map
        self.map[id] = self.counter
        self.counter += 1


def _get(e, key):
    return e.find(key).text


def anime(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('anime'):
        id = _get(e, 'series_animedb_id')
        ids.add(id)
        x = [ids.map[id]] + [_get(e, x) for x in (
            'series_title', 'series_type', 'series_episodes',
            'series_animedb_id',
        )]
        logger.debug(x)
        yield x


def myanime(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('anime'):
        id = _get(e, 'series_animedb_id')
        x = [ids.map[id]] + [_get(e, x).lower() for x in (
            'my_watched_episodes', 'my_status', 'my_start_date',
            'my_finish_date',
        )]
        x[-3] = stat_map[x[-3]]
        if x[-2] == '0000-00-00':
            x[-2] = None
        if x[-1] == '0000-00-00':
            x[-1] = None
        logger.debug(x)
        yield x


def main(config, file):
    with mysqllib.connect(**config['db_args']) as cur:
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
        )), list(anime(ids, file)))
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
        )), list(myanime(ids, file)))

if __name__ == '__main__':
    main()
