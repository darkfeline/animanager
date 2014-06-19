import logging
import sys
from datetime import date

from animanager import mysqllib
from animanager import inputlib

logger = logging.getLogger(__name__)


def main(config, name=None):
    with mysqllib.connect(**config['db_args']) as cur:

        # get choices
        if not name:
            name = input("Find an anime: ")
        assert isinstance(name, str)
        cur.execute(
            'SELECT id, name FROM anime WHERE name LIKE %s',
            ('%'+name+'%',))
        results = cur.fetchall()
        try:
            i = inputlib.get_choice(results)
        except inputlib.Cancel:
            print('Quitting')
            sys.exit(1)
        id = results[i][0]

        # Get eps and confirm
        cur.execute(' '.join((
            'SELECT ep_watched, ep_total FROM anime',
            'WHERE id=%s')), (id,))
        watched, total = cur.fetchone()
        print('Bumping {}/{}'.format(watched, total))
        if watched >= total and total != 0:
            print('Maxed')
            sys.exit(1)
        confirm = input("Okay? [Y/n]")
        if confirm.lower() in ('n', 'no'):
            print('Quitting')
            sys.exit(1)
        watched += 1

        # Set status if needed
        cur.execute('SELECT status FROM anime WHERE id=%s', (id,))
        status = list(cur.fetchone()[0])[0]  # mysqllib returns set b/c retard
        assert isinstance(status, str)
        if status in ('on hold', 'dropped'):
            confirm = input("Status is {}; set watching? [Y/n]".format(status))
            if confirm.lower() not in ('n', 'no'):
                print('Setting watching')
                cur.execute(
                    'UPDATE anime SET status=%s WHERE id=%s',
                    ('watching', id))
        elif status in ('plan to watch',):
            print('Status is {}, setting watching and start date'.format(
                status))
            cur.execute(
                'UPDATE anime SET status=%s, date_started=%s WHERE id=%s',
                ('watching', date.today().isoformat(), id))

        # Set new value
        cur.execute(
            'UPDATE anime SET ep_watched=%s WHERE id=%s',
            (watched, id))
        print('Now {}/{}'.format(watched, total))

        # Set complete if needed
        if watched == total and total != 0:
            print('Setting complete')
            cur.execute(' '.join((
                'UPDATE anime SET status=%s, date_finished=%s',
                'WHERE id=%s',
                )), ('complete', date.today().isoformat(), id))
