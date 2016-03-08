"""Output items missing AIDs for manual handling."""

import logging

from dblib import anime
from paths import OLD


def main():
    logging.basicConfig(level='DEBUG',
                        format='%(asctime)s:%(levelname)s:%(message)s')

    conn = anime.connect(OLD)
    cur = conn.execute('SELECT * FROM anime WHERE anidb_id IS NULL')

    for row in cur:
        print(list(row))


if __name__ == '__main__':
    main()
