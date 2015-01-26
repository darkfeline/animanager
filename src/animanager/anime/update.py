import logging
from urllib.error import URLError
from urllib.parse import urlencode

from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/anime/search.xml?"
statuses = ['plan to watch', 'watching', 'complete']


def _get_datum(entity, key):
    return entity.find(key).text

_data_keys = ('id', 'title', 'episodes')

def _get_data(entity):
    return [_get_datum(entity, key) for key in _data_keys]


def anime_iter(config):
    """Return a generator of anime database entries."""
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(' '.join((
            'SELECT id, animedb_id, name, ep_total FROM anime',
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
    """Update anime database entries."""
    with mysqllib.connect(**config["db_args"]) as cur:
        print('Setting episode totals')
        cur.executemany('UPDATE anime SET ep_total=%s WHERE id=%s', to_update)
        print('Setting complete as needed')
        cur.execute(' '.join((
            'UPDATE anime SET status="complete"',
            'WHERE ep_total = ep_watched AND ep_total != 0',
        )))


def main(args):
    config = args.config
    to_update = []
    for id, mal_id, name, my_eps in anime_iter(config):
        # Search for our show on MAL, and make sure to match our MAL id.
        logger.debug("Our entry id=%r, name=%r, eps=%r", id, name, my_eps)
        response = ffrequest(mal_search + urlencode({'q': name}))
        response = response.read().decode()
        logger.debug(response)
        tree = xmllib.parse(response)
        if tree is None:
            logger.warning('No results found for id=%r, name=%r', id, name)
            continue
        found = [_get_data(entity) for entity in list(tree)]
        found = dict((int(entry[0]), entry[1:]) for entry in found)
        found_title, found_eps = found[mal_id]
        found_eps = int(found_eps)
        logger.debug('Found mal_id=%r, name=%r, eps=%r',
                     mal_id, found_title, found_eps)
        if found_title != name:
            raise Error('Found {}, our name is {}'.format(
                found_title, name))
        if found_eps != 0:
            assert found_eps > 0
            to_update.append((found_eps, id))
    logger.info('Updating local entries')
    update_entries(config, to_update)


class Error(Exception):
    pass
