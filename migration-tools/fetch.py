"""Fetch data from AniDB and store locally."""

import time
import logging
import os
import sqlite3

import anidb
import relish
from paths import OLD, ANIDB


def main():
    logging.basicConfig(level='DEBUG',
                        format='%(asctime)s:%(levelname)s:%(message)s')

    if not os.path.exists('aids.pickle'):
        conn = sqlite3.connect(OLD)
        cur = conn.cursor()
        cur.execute('SELECT anidb_id FROM anime')
        aids = cur.fetchall()
        aids = [x[0] for x in aids if x[0]]
        aids = sorted(aids)
        relish.dump(aids, 'aids.pickle')
    else:
        aids = relish.load('aids.pickle')

    for aid in aids:
        aid_file = os.path.join(ANIDB, '{}.xml'.format(aid))
        if os.path.exists(aid_file):
            logging.info('Skipping %s', aid)
            continue

        response = anidb.LookupRequest(aid).open()
        tree = response.tree()
        tree.write(aid_file)
        logging.info('Added %s', aid)
        time.sleep(240)


if __name__ == '__main__':
    main()
