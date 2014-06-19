#!/usr/bin/env python

from xml.etree import ElementTree
import logging
from itertools import count

from animanager import mysqllib

logger = logging.getLogger(__name__)

stat_map = {
    'reading': 'reading',
    'completed': 'complete',
    'plan to read': 'plan to read',
    'on-hold': 'on hold',
    'dropped': 'dropped',
}


def _get(e, key):
    return e.find(key).text


def manga(ids, file):
    id_counter = count(1)
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('manga'):
        fields = dict()
        fields['id'] = next(id_counter)
        fields.update(
            [(our_field, _get(e, their_field)) for our_field, their_field in (
                ('name', 'manga_title'),
                ('vol_read', 'my_read_volumes'),
                ('vol_total', 'manga_volumes'),
                ('ch_read', 'my_read_chapters'),
                ('ch_total', 'manga_chapters'),
                ('status', 'my_status'),
                ('date_started', 'my_start_date'),
                ('date_finished', 'my_finish_date'),
                ('mangadb_id', 'manga_mangadb_id'),
            )])
        fields['status'] = stat_map[fields['status'].lower()]
        if fields['date_started'] == '0000-00-00':
            fields['date_started'] = None
        if fields['date_finished'] == '0000-00-00':
            fields['date_finished'] = None
        logger.debug(fields)
        yield fields


FIELDS = [
    'id',
    'name',
    'vol_read',
    'vol_total',
    'ch_read',
    'ch_total',
    'status',
    'date_started',
    'date_finished',
    'mangadb_id',
]


def main(config, file):
    with mysqllib.connect(**config['db_args']) as cur:
        cur.execute('INSERT INTO manga ({}) VALUES {}'.format(
            ', '.join(FIELDS),
            ', '.join(
                '({})'.format(', '.join(entry[field] for field in FIELDS))
                for entry in manga(file))))

if __name__ == '__main__':
    main()
