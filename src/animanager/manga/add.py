import logging
from datetime import date
from urllib.parse import urlencode

from animanager import inputlib
from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/manga/search.xml?"
statuses = ('plan to read', 'reading', 'complete')


def _get(e, key):
    return e.find(key).text


def main(config, name=None):

    # Get choices from MAL API
    if not name:
        name = input("Search for: ")
    response = ffrequest(mal_search + urlencode({'q': name}))
    response = response.read().decode()
    tree = xmllib.parse(response)
    found = [
        [_get(e, k) for k in ('id', 'title', 'chapters', 'volumes', 'type')]
        for e in list(tree)]
    i = inputlib.get_choice(['{} {} ({})'.format(id, title, type) for id,
                             title, ch, vol, type in found])

    # Accumulate fields
    args = {}
    args.update(
        zip(['mangadb_id', 'name', 'ch_total', 'vol_total', 'type'], found[i]))

    i = inputlib.get_choice(statuses, 0)
    args['status'] = statuses[i]

    if args['status'] == 'reading':
        x = input('Set start date to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
    elif args['status'] == 'complete':
        args['ch_watched'] = args['ch_total']
        args['vol_watched'] = args['vol_total']
        x = input('Set dates to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
            args['date_finished'] = date.today().isoformat()

    # add manga entry
    with mysqllib.connect(**config["db_args"]) as cur:
        fields = list(args)
        cur.execute(
            'INSERT INTO manga SET {}'.format(
                ', '.join(x+'=%s' for x in fields)),
            [args[x] for x in fields])
