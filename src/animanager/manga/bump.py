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
            name = input("Find a manga: ")
        assert isinstance(name, str)
        cur.execute(
            'SELECT id, name FROM manga WHERE name LIKE %s',
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
            'SELECT ch_read, ch_total FROM manga',
            'LEFT JOIN mymanga ON manga.id=mymanga.id',
            'WHERE manga.id=%s')), (id,))
        read, total = cur.fetchone()
        print('Bumping {}/{}'.format(read, total))
        if read >= total and total != 0:
            print('Maxed')
            sys.exit(1)
        confirm = input("Okay? [Y/n]")
        if confirm.lower() in ('n', 'no'):
            print('Quitting')
            sys.exit(1)
        read += 1

        # Set status if needed
        cur.execute('SELECT status FROM mymanga WHERE id=%s', (id,))
        status = list(cur.fetchone()[0])[0]  # mysqllib returns set b/c retard
        assert isinstance(status, str)
        if status in ('on hold', 'dropped'):
            confirm = input("Status is {}; set reading? [Y/n]".format(status))
            if confirm.lower() not in ('n', 'no'):
                print('Setting reading')
                cur.execute(
                    'UPDATE mymanga SET status=%s WHERE id=%s',
                    ('reading', id))
        elif status in ('plan to read',):
            print('Status is {}, setting reading and start date'.format(
                status))
            cur.execute(
                'UPDATE mymanga SET status=%s, date_started=%s WHERE id=%s',
                ('reading', date.today().isoformat(), id))

        # Set new value
        cur.execute(
            'UPDATE mymanga SET ch_read=%s WHERE id=%s',
            (read, id))
        print('Now {}/{}'.format(read, total))

        # Set complete if needed
        if read == total and total != 0:
            print('Setting complete')
            cur.execute(' '.join((
                'UPDATE mymanga SET status=%s, date_finished=%s',
                'WHERE id=%s',
                )), ('complete', date.today().isoformat(), id))
