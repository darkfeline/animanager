import logging
import sys

from animanager import inputlib
from animanager import mysqllib

logger = logging.getLogger(__name__)


def main(config, name=None):
    if not name:
        name = input("Find an anime: ")
    with mysqllib.connect(**config.db_args) as cur:
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
        i = inputlib.get_choi(results)
        id = results[i][0]
        cur.execute('UPDATE myanime SET status="on hold" WHERE id=%s', (id,))
        print('Set to on hold')
