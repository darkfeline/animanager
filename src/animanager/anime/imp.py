#!/usr/bin/env python

from xml.etree import ElementTree
import logging
from itertools import count

from animanager import mysqllib

logger = logging.getLogger(__name__)

stat_map = {
    'watching': 'watching',
    'completed': 'complete',
    'plan to watch': 'plan to watch',
    'on-hold': 'on hold',
    'dropped': 'dropped',
}


def _get(e, key):
    return e.find(key).text


def anime(file):
    id_counter = count(1)
    tree = ElementTree.parse(file)
    root = tree.getroot()
    for e in root.iter('anime'):
        fields = dict()
        fields['id'] = next(id_counter)
        fields.update(
            [(our_field, _get(e, their_field)) for our_field, their_field in (
                ('name', 'series_title'),
                ('type', 'series_type'),
                ('ep_watched', 'my_watched_episodes'),
                ('ep_total', 'series_episodes'),
                ('status', 'my_status'),
                ('date_started', 'my_start_date'),
                ('date_finished', 'my_finish_date'),
                ('animedb_id', 'series_animedb_id'),
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
    'type',
    'ep_watched',
    'ep_total',
    'status',
    'date_started',
    'date_finished',
    'animedb_id',
]


def main(config, file):
    with mysqllib.connect(**config['db_args']) as cur:
        cur.execute('INSERT INTO anime ({}) VALUES {}'.format(
            ', '.join(FIELDS),
            ', '.join(
                '({})'.format(', '.join(entry[field] for field in FIELDS))
                for entry in anime(file))))

if __name__ == '__main__':
    main()
