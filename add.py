#!/usr/bin/env python

import logging
from datetime import date
from urllib.parse import urlencode
from xml.etree import ElementTree
import html.parser
import re
import sys

import mysqllib
import requestlib
from requestlib import ffrequest

import info

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/anime/search.xml?"
stati = ['plan to watch', 'watching', 'complete']


def _get(e, key):
    return e.find(key).text


def main():

    logging.basicConfig(level=logging.DEBUG)

    requestlib.setup()

    # MAL API
    partial = input("Search for: ")
    print(mal_search + urlencode({'q': partial}))
    response = ffrequest(mal_search + urlencode({'q': partial}))
    h = html.parser.HTMLParser()
    response = response.read().decode()
    response = h.unescape(response)
    # due to some bug, there are double entities? e.g. &amp;amp;
    response = re.sub(r'&.+?;', '', response)
    tree = ElementTree.fromstring(response)
    found = [
        [_get(e, k) for k in ('id', 'title', 'episodes', 'type')]
        for e in list(tree)]
    for i, e in enumerate(found):
        print('{}: {}'.format(i, e[1]))

    # add anime entry
    i = int(input('Pick: '))
    animedb_id, name, ep_total, type = found[i]
    with mysqllib.connect(**info.db_args) as cur:
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
        query = ', '.join((query, 'date_started=%s'))
        args.append(date.today().isoformat())
    elif status == 'complete':
        query = ', '.join((query, 'ep_watched=%s'))
        args.append(ep_total)
    with mysqllib.connect(**info.db_args) as cur:
        cur.execute(query, args)

if __name__ == '__main__':
    main()
