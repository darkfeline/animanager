import logging

import locator
import globals


def find():

    logging.debug('find()')
    print('Which entry to find?')

    a = input(globals.PROMPT)
    entry = locator.db.get(a)
    logging.debug(entry)
    if entry is None:
        print('Cannot find {}'.format(a))
        return -1
    else:
        print(_format_entry(entry))
        return -1


def _format_entries(entries):
    return [_format_entry(entry) for entry in entries]


def _format_entry(entry):
    map = dict((globals.FIELDS[i], entry[i]) for i in range(len(entry)))
    return globals.ENTRY.format(**map)
