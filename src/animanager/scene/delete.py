import logging

from animanager import gvars
from animanager import locator
from animanager.scene import choose

logger = logging.getLogger(__name__)


def find():

    logger.debug('find()')
    print('Which entry to delete?')

    a = input(gvars.PROMPT)
    locator.stack.add((delete, [a], {}))


def search():

    logger.debug('search()')
    print('Search for what?')

    a = input(gvars.PROMPT)
    entries = locator.db.search(a)
    logger.debug('Found {}'.format(entries))

    if not entries:
        print('Cannot find {}'.format(a))
        return -2
    else:
        locator.stack.add((choose.choose_entry, [entries, delete], {}))


def delete(key):

    logger.debug('delete(%s)', key)
    print('Really delete {}? (yes/no)'.format(key))

    a = input(gvars.PROMPT).lower()
    if a == 'yes':
        locator.db.delete(key)
        print('Deleted {}'.format(key))
        return -2
    elif a == 'no':
        print('Not deleting')
        return -2
    else:
        print('Please type yes or no')
