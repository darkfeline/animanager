import logging

from animanager import globals
from animanager import locator

logger = logging.getLogger(__name__)


def _delete(key):
    try:
        locator.db.delete(key)
    except Exception as e:
        raise e
    else:
        print('Deleted {}'.format(key))


def find():

    logger.debug('delete.find()')
    print('Which entry to delete?')

    a = input(globals.PROMPT)
    _delete(a)
    return -2


def search():

    logger.debug('delete.search()')
    print('Search for what?')

    a = input(globals.PROMPT)
    entries = locator.db.search(a)
    logger.debug('Found {}'.format(entries))

    if not entries:
        print('Cannot find {}'.format(a))
        return -2
    else:
        locator.stack.add((search_choose, [entries], {}))


def search_choose(entries):

    logger.debug('change.search_choose({})'.format(entries))
    for i, entry in enumerate(entries):
        print('{} - {}'.format(i, entry[0]))
    print('q - quit')
    print()
    print('Which entry to delete?')

    a = input(globals.PROMPT)
    if a == 'q':
        print("Okay")
        return -2
    else:
        try:
            key = entries[int(a)][0]
            logger.debug('Got key %s', key)
        except IndexError:
            print('Bad input {}'.format(a))
            return
        else:
            _delete(key)
