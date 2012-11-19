import logging

from animanager import locator
from animanager import globals

logger = logging.getLogger(__name__)


def find():

    logger.debug('find()')
    print('Which entry to find?')

    a = input(globals.PROMPT)
    entry = locator.db.get(a)
    logger.debug('Found {}'.format(entry))
    if entry is None:
        print('Cannot find {}'.format(a))
        return -2
    else:
        print(_format_entry(entry))
        return -2


def search():

    logger.debug('search()')
    print('Search for what?')

    a = input(globals.PROMPT)
    entries = locator.db.search(a)
    logger.debug('Found {}'.format(entries))
    if not entries:
        print('Cannot find {}'.format(a))
        return -2
    else:
        for a in _format_entries(entries):
            print(a)
        return -2


def _format_entries(entries):
    return [_format_entry(entry) for entry in entries]


def _format_entry(entry):
    map = dict((globals.FIELDS[i], entry[i]) for i in range(len(entry)))
    return globals.ENTRY.format(**map)
