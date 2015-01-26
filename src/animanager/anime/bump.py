from collections import OrderedDict
from datetime import date
import logging
import sys

from animanager import mysqllib
from animanager import inputlib

logger = logging.getLogger(__name__)


def main(args):
    config = args.config
    name = args.name
    with mysqllib.connect(**config['db_args']) as cur:

        # Get choices from database
        cur.execute(' '.join((
            'SELECT id, name FROM anime',
            'WHERE name LIKE %s AND status != "complete"',
        )), ('%{}%'.format(name),))
        results = cur.fetchall()
        choice_i = inputlib.get_choice(
            ['{} {}'.format(x[0], x[1]) for x in results])
        choice_id = results[choice_i][0]

        # Get data and confirm action
        cur.execute(' '.join((
            'SELECT ep_watched, ep_total, status FROM anime',
            'WHERE id=%s')), (choice_id,))
        watched, total, status = cur.fetchone()
        if watched >= total and total != 0:
            print('Maxed')
            sys.exit(1)
        print('Bumping {}/{}'.format(watched, total))
        confirm = input("Okay? [Y/n]")
        if confirm.lower() in ('n', 'no'):
            print('Quitting')
            sys.exit(1)

        # MySQL connector returns a set type because it is retarded.
        # We need to convert it.
        status = list(status)
        assert len(status) == 1
        status = status[0]
        assert isinstance(status, str)

        # Calculate what needs updating
        update_map = OrderedDict()
        watched += 1
        print('Now {}/{}'.format(watched, total))
        update_map['ep_watched'] = watched

        if status in ('on hold', 'dropped', 'plan to watch'):
            print('Setting status to "watching"')
            update_map['status'] = 'watching'
        if status == 'plan to watch':
            print('Setting start date')
            update_map['date_started'] = date.today().isoformat()
        if watched == total and total != 0:
            print('Setting status to "complete"')
            update_map = ['status'] = 'complete'

        query_string = 'UPDATE anime SET {} WHERE id=%s'.format(
            ', '.join('{}=%s'.format(key for key in update_map))
        )
        query_args = list(update_map.values()) + [choice_id]

        cur.execute(query_string, query_args)
