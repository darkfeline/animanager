import logging

from animanager import locator
from animanager import gvars
from animanager.scene import choose

logger = logging.getLogger(__name__)


def match():

    logger.debug('match()')
    print('Check which entry?')

    a = input(gvars.PROMPT)
    locator.stack.add((_print_entry, [a], {}))


def _print_entry(key):
    entry = locator.db.get(key)
    logger.debug('Found %s', entry)
    if entry:
        print(_format_entry(entry))
    else:
        print('{} not found'.format(key))
    return -2


def find():

    logger.debug('find()')
    print('Search for what?')

    a = input(gvars.PROMPT)
    entries = locator.db.search(a)
    logger.debug('Found {}'.format(entries))
    if not entries:
        print('Cannot find {}'.format(a))
        return -2
    else:
        locator.stack.add((choose.choose_entry, [entries, _print_entry], {}))


def _format_entry(entry):
    map = dict((gvars.FIELDS[i], entry[i]) for i in range(len(entry)))
    return gvars.ENTRY.format(**map)
