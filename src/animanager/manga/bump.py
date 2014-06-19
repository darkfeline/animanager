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
            'SELECT id, name, type FROM manga WHERE name LIKE %s',
            ('%'+name+'%',))
        results = cur.fetchall()
        try:
            # type is a set here because stupid
            i = inputlib.get_choice([
                (id, '{} ({})'.format(title, list(type)[0])) for
                id, title, type in results])
        except inputlib.Cancel:
            print('Quitting')
            sys.exit(1)
        id = results[i][0]

        # Get eps and confirm
        cur.execute(' '.join((
            'SELECT ch_read, ch_total, vol_total FROM manga',
            'WHERE id=%s')), (id,))
        ch_read, ch_total, vol_total = cur.fetchone()
        print('Bumping {}/{}'.format(ch_read, ch_total))
        if ch_read >= ch_total and ch_total != 0:
            print('Maxed')
            sys.exit(1)
        confirm = input("Okay? [Y/n]")
        if confirm.lower() in ('n', 'no'):
            print('Quitting')
            sys.exit(1)
        ch_read += 1

        # Set status if needed
        cur.execute('SELECT status FROM manga WHERE id=%s', (id,))
        status = list(cur.fetchone()[0])[0]  # mysqllib returns set b/c retard
        assert isinstance(status, str)
        if status in ('on hold', 'dropped'):
            confirm = input("Status is {}; set reading? [Y/n]".format(status))
            if confirm.lower() not in ('n', 'no'):
                print('Setting reading')
                cur.execute(
                    'UPDATE manga SET status=%s WHERE id=%s',
                    ('reading', id))
        elif status in ('plan to read',):
            print('Status is {}, setting reading and start date'.format(
                status))
            cur.execute(
                'UPDATE manga SET status=%s, date_started=%s WHERE id=%s',
                ('reading', date.today().isoformat(), id))

        # Set new value
        cur.execute(
            'UPDATE manga SET ch_read=%s WHERE id=%s',
            (ch_read, id))
        print('Now {}/{}'.format(ch_read, ch_total))

        # Set complete if needed
        if ch_read == ch_total and ch_total != 0:
            print('Setting complete')
            cur.execute(' '.join((
                'UPDATE manga SET status=%s, date_finished=%s, vol_read=%s',
                'WHERE id=%s',
                )), ('complete', date.today().isoformat(), vol_total, id))
