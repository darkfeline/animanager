import logging
import sys

from animanager import inputlib
from animanager import mysqllib

logger = logging.getLogger(__name__)


def main(config, name=None):
    if not name:
        name = input("Find an anime: ")
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(' '.join((
            'SELECT id, name FROM anime',
            'WHERE status IN ("watching", "on hold")',
            'AND name LIKE %s',
        )), ('%'+name+'%',))
        results = cur.fetchall()
        if not results:
            print("Found nothing")
            sys.exit(1)
        i = inputlib.get_choice(['{} {}'.format(x[0], x[1]) for x in results])
        id = results[i][0]
        cur.execute('UPDATE anime SET status="dropped" WHERE id=%s', (id,))
        print('Set to dropped')
