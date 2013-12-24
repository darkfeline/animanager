#!/usr/bin/env python

import logging
import sys
from datetime import date

import mysqllib

import info

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    with mysqllib.connect(**info.db_args) as cur:
        name = input("Find an anime: ")
        cur.execute(' '.join((
            'SELECT myanime.id, name FROM anime',
            'LEFT JOIN myanime ON anime.id=myanime.id',
            'WHERE status="watching"',
            'AND name LIKE %s',
        )), ('%'+name+'%',))
        results = cur.fetchall()
        if not results:
            print("Found nothing")
            sys.exit(1)
        for i, series in enumerate(results):
            print("{} - {}: {}".format(i, series[0], series[1]))
        i = int(input("Pick one\n"))
        confirm = input("{}: {}\nOkay? [Y/n]".format(
            results[i][0], results[i][1]))
        if confirm.lower() in ('n', 'no'):
            print('Quitting')
            sys.exit(1)
        id = results[i][0]
        cur.execute('UPDATE myanime SET status="on hold" WHERE id=%s', (id,))
        print('Set to on hold')

if __name__ == '__main__':
    main()
