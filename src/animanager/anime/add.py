import logging
from datetime import date
from urllib.parse import urlencode

from animanager import inputlib
from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

mal_search = "http://myanimelist.net/api/anime/search.xml?"
statuses = ('plan to watch', 'watching', 'complete')


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
        [_get(e, k) for k in ('id', 'title', 'episodes', 'type')]
        for e in list(tree)]
    i = inputlib.get_choice(found)

    # Accumulate fields
    args = {}
    args.update(
        zip(['animedb_id', 'name', 'ep_total', 'type'], found[i]))

    for i, x in enumerate(statuses):
        print('{}: {}'.format(i, x))
    i = int(input('Pick status: '))
    args['status'] = statuses[i]

    if args['status'] == 'watching':
        x = input('Set start date to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
    elif args['status'] == 'complete':
        args['ep_watched'] = args['ep_total']
        x = input('Set dates to today? [Y/n]')
        if x.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
            args['date_finished'] = date.today().isoformat()

    # add anime entry
    with mysqllib.connect(**config["db_args"]) as cur:
        fields = list(args)
        cur.execute(
            'INSERT INTO anime SET {}'.format(
                ', '.join(x+'=%s' for x in fields)),
            [args[x] for x in fields])
