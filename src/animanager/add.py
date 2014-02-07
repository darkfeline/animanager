import logging
from datetime import date
from urllib.parse import urlencode
from xml.etree import ElementTree
import sys

from animanager import inputlib
from animanager import mysqllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/anime/search.xml?"
stati = ('plan to watch', 'watching', 'complete')


def _get(e, key):
    return e.find(key).text


def main(config, name=None):

    # MAL API
    if not name:
        name = input("Search for: ")
    response = ffrequest(mal_search + urlencode({'q': name}))
    response = response.read().decode()
    tree = ElementTree.fromstring(response)
    found = [
        [_get(e, k) for k in ('id', 'title', 'episodes', 'type')]
        for e in list(tree)]
    i = inputlib.get_choice(found)

    # add anime entry
    animedb_id, name, ep_total, type = found[i]
    with mysqllib.connect(**config["db_args"]) as cur:
        response = cur.execute('SELECT id FROM anime WHERE name=%s', (name,))
        if cur.fetchone():
            print("Already added")
            sys.exit(1)
        print("Adding main entry")
        cur.execute(' '.join((
            'INSERT INTO anime (name, type, ep_total, animedb_id)',
            'VALUES',
            '(%s, %s, %s, %s)',
            )), (name, type, ep_total, animedb_id))
        response = cur.execute('SELECT id FROM anime WHERE name=%s', (name,))
        id = cur.fetchone()[0]

    # add myanime entry
    print("Status:")
    for i, x in enumerate(stati):
        print('{}: {}'.format(i, x))
    i = int(input('Pick: '))
    status = stati[i]
    args = [id, status]
    query = 'INSERT INTO myanime SET id=%s, status=%s'
    if status == 'watching':
        x = input('Set start date to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            query = ', '.join((query, 'date_started=%s'))
            args.append(date.today().isoformat())
    elif status == 'complete':
        query = ', '.join((query, 'ep_watched=%s'))
        args.append(ep_total)
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(query, args)
