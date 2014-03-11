import logging
from datetime import date
from urllib.parse import urlencode
import sys

from animanager import inputlib
from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/manga/search.xml?"
stati = ('plan to watch', 'reading', 'complete')


def _get(e, key):
    return e.find(key).text


def main(config, name=None):

    # MAL API
    if not name:
        name = input("Search for: ")
    response = ffrequest(mal_search + urlencode({'q': name}))
    response = response.read().decode()
    tree = xmllib.parse(response)
    if tree is None:
        sys.exit(1)
    found = [
        [_get(e, k) for k in ('id', 'title', 'chapters', 'volumes', 'type')]
        for e in list(tree)]
    i = inputlib.get_choice([
        (id, '{} ({})'.format(title, type)) for
        id, title, ch, vol, type in found])

    # add manga entry
    mangadb_id, name, ch_total, vol_total, type = found[i]
    with mysqllib.connect(**config["db_args"]) as cur:
        response = cur.execute(
            'SELECT id FROM manga WHERE mangadb_id=%s', (mangadb_id,))
        if cur.fetchone():
            print("Already added")
            sys.exit(1)
        print("Adding main entry")
        cur.execute(' '.join((
            'INSERT INTO manga (name, type, ch_total, vol_total, mangadb_id)',
            'VALUES',
            '(%s, %s, %s, %s, %s)',
            )), (name, type, ch_total, vol_total, mangadb_id))
        response = cur.execute(
            'SELECT id FROM manga WHERE mangadb_id=%s', (mangadb_id,))
        id = cur.fetchone()[0]

    # add mymanga entry
    print("Status:")
    for i, x in enumerate(stati):
        print('{}: {}'.format(i, x))
    i = int(input('Pick: '))
    status = stati[i]
    args = [id, status]
    query = 'INSERT INTO mymanga SET id=%s, status=%s'
    if status == 'reading':
        x = input('Set start date to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            query = ', '.join((query, 'date_started=%s'))
            args.append(date.today().isoformat())
    elif status == 'complete':
        query = ', '.join((query, 'ch_watched=%s'))
        args.append(ch_total)
        query = ', '.join((query, 'vol_watched=%s'))
        args.append(vol_total)
        x = input('Set dates to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            query = ', '.join((query, 'date_started=%s', 'date_finished=%s'))
            args.extend([date.today().isoformat()] * 2)
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(query, args)
