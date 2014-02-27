#!/usr/bin/env python

from xml.etree import ElementTree
import logging

from animanager import mysqllib

logger = logging.getLogger(__name__)

stat_map = {
    'reading': 'reading',
    'completed': 'complete',
    'plan to read': 'plan to read',
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


def manga(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('manga'):
        id = _get(e, 'manga_mangadb_id')
        ids.add(id)
        x = [ids.map[id]] + [_get(e, x) for x in (
            'manga_title', 'manga_volumes', 'manga_chapters',
            'manga_mangadb_id',
        )]
        logger.debug(x)
        yield x


def mymanga(ids, file):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('manga'):
        id = _get(e, 'manga_mangadb_id')
        x = [ids.map[id]] + [_get(e, x).lower() for x in (
            'my_read_volumes', 'my_read_chapters', 'my_status',
            'my_start_date', 'my_finish_date',
        )]
        x[-3] = stat_map[x[-3]]
        if x[-2] == '0000-00-00':
            x[-2] = None
        if x[-1] == '0000-00-00':
            x[-1] = None
        logger.debug(x)
        yield x


def main(config, file):
    # from pprint import pprint
    # ids = IDCounter()
    # pprint(list(manga(ids, file)))
    # pprint(list(mymanga(ids, file)))
    # import sys; sys.exit()
    with mysqllib.connect(**config['db_args']) as cur:
        ids = IDCounter()
        cur.executemany(' '.join((
            'INSERT INTO manga',
            '(' + ', '.join((
                'id',
                'name',
                'vol_total',
                'ch_total',
                'mangadb_id',
            )) + ')',
            'VALUES',
            '(%s, %s, %s, %s, %s)',
        )), list(manga(ids, file)))
        cur.executemany(' '.join((
            'INSERT INTO mymanga',
            '(' + ', '.join((
                'id',
                'vol_read',
                'ch_read',
                'status',
                'date_started',
                'date_finished',
            )) + ')'
            'VALUES',
            '(%s, %s, %s, %s, %s, %s)',
        )), list(mymanga(ids, file)))

if __name__ == '__main__':
    main()
