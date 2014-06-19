import logging
from urllib.error import URLError
from urllib.parse import urlencode

from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/manga/search.xml?"
statuses = ['plan to read', 'reading', 'complete']


def _get(e, key):
    return e.find(key).text


def manga_iter(config):
    """Generator for manga to recheck"""
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(' '.join((
            'SELECT id, mangadb_id, name, ch_total, vol_total',
            'FROM manga',
            'WHERE ch_total = 0',
            'OR vol_total = 0',
            'OR type = ""',
            'OR status = "reading"',
        )))
        while True:
            x = cur.fetchone()
            if x:
                yield x
            else:
                break


def update_entries(config, to_update):
    with mysqllib.connect(**config["db_args"]) as cur:
        print('Setting ch/vol totals')
        cur.executemany(' '.join((
            'UPDATE manga SET ch_total=%s, vol_total=%s',
            'WHERE id=%s')),
            to_update)
        print('Setting complete as needed')
        cur.execute(' '.join((
            'UPDATE manga SET status="complete" WHERE',
            '(ch_total = ch_read AND ch_total != 0) OR',
            '(vol_total=vol_read AND vol_total != 0)',
        )))


def main(config):

    to_update = []

    # MAL API
    for id, mal_id, name, my_chs, my_vols in manga_iter(config):
        while True:
            try:
                response = ffrequest(mal_search + urlencode({'q': name}))
            except URLError:
                continue
            else:
                break
        tree = xmllib.parse(response.read().decode())
        found = dict((
            int(_get(e, 'id')),
            [_get(e, k) for k in ('title', 'chapters', 'volumes')]
        ) for e in list(tree))
        found_title, found_chs, found_vols = found[mal_id]
        found_chs = int(found_chs)
        found_vols = int(found_vols)
        logger.debug("Name: %r, Ch: %r, Vol: %r", name, my_chs, my_vols)
        logger.debug('Found id=%r, mal_id=%r, name=%r, ch=%r, vol=%r',
                     id, mal_id, found_title, found_chs, found_vols)
        assert found_title == name
        if found_chs != 0 or found_vols != 0:
            to_update.append((found_chs, found_vols, id))

    logger.info('Updating local entries')
    update_entries(config, to_update)
