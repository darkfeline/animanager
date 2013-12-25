import logging
from urllib.error import URLError
from urllib.parse import urlencode
from xml.etree import ElementTree
import html.parser

from animanager import mysqllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/anime/search.xml?"
stati = ['plan to watch', 'watching', 'complete']


def _get(e, key):
    return e.find(key).text


def anime_iter(config):
    """Generator for anime to recheck"""
    with mysqllib.connect(**config.db_args) as cur:
        cur.execute(' '.join((
            'SELECT anime.id, animedb_id, name, ep_total FROM anime',
            'LEFT JOIN myanime ON myanime.id = anime.id',
            'WHERE ep_total = 0',
            'OR status = "watching"',
        )))
        while True:
            x = cur.fetchone()
            if x:
                yield x
            else:
                break


def update_entries(config, to_update):
    with mysqllib.connect(**config.db_args) as cur:
        print('Setting episode totals')
        cur.executemany('UPDATE anime SET ep_total=%s WHERE id=%s', to_update)
        print('Setting complete as needed')
        cur.execute(' '.join((
            'UPDATE anime',
            'LEFT JOIN myanime ON anime.id=myanime.id',
            'SET status="complete" WHERE ep_total=ep_watched',
        )))


def main(config):

    to_update = []

    # MAL API
    h = html.parser.HTMLParser()
    for id, mal_id, name, my_eps in anime_iter(config):
        while True:
            try:
                response = ffrequest(mal_search + urlencode({'q': name}))
            except URLError:
                continue
            else:
                break
        response = h.unescape(response.read().decode())
        tree = ElementTree.fromstring(response)
        found = dict((int(_get(e, 'id')),
                      [_get(e, k) for k in ('title', 'episodes')])
                     for e in list(tree))
        found_title, found_eps = found[mal_id]
        found_eps = int(found_eps)
        logging.debug("Name: %r, Eps: %r", name, my_eps)
        logger.debug('Found id=%r, mal_id=%r, name=%r, eps=%r',
                     id, mal_id, name, found_eps)
        assert found_title == name
        if found_eps != 0:
            assert found_eps > 0
            to_update.append((found_eps, id))

    logger.info('Updating local entries')
    update_entries(config, to_update)
