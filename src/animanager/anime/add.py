from collections import OrderedDict
from datetime import date
import logging
from urllib.parse import urlencode

from animanager import inputlib
from animanager import mysqllib
from animanager import xmllib
from animanager.requestlib import ffrequest

logger = logging.getLogger(__name__)

MAL_SEARCH = "http://myanimelist.net/api/anime/search.xml?"
statuses = ('plan to watch', 'watching', 'complete')


def _get_datum(entity, key):
    return entity.find(key).text

_data_keys = ('id', 'title', 'episodes', 'type')

def _get_data(entity):
    return [_get_datum(entity, key) for key in _data_keys]


def main(args):

    config = args.config
    name = args.name

    # Get choices from MAL API
    response = ffrequest(MAL_SEARCH + urlencode({'q': name}))
    response = response.read().decode()
    tree = xmllib.parse(response)
    found = [_get_data(entity) for entity in list(tree)]
    i = inputlib.get_choice(['{} {}'.format(x[0], x[1]) for x in found])

    # Set data fields
    args = OrderedDict(zip(['animedb_id', 'name', 'ep_total', 'type'],
                           found[i]))

    i = inputlib.get_choice(statuses, 0)
    args['status'] = statuses[i]

    if args['status'] == 'watching':
        confirm = input('Set start date to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            args['date_started'] = date.today().isoformat()
    elif args['status'] == 'complete':
        args['ep_watched'] = args['ep_total']
        confirm = input('Set dates to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            today = date.today().isoformat()
            args['date_started'] = today
            args['date_finished'] = today

    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute(
            'INSERT INTO anime SET {}'.format(
                ', '.join('{}=%s'.format(key) for key in args)),
            args.values())
