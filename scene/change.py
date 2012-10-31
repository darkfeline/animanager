import logging

import globals
import locator


def change_find():

    logging.debug('change_find()')
    print('Which entry to change?')

    a = input(globals.PROMPT)
    entry = locator.db.get(a)
    if entry is None:
        print('Cannot find {}'.format(a))
        return -1
    else:
        return (change_choose, [a], {})


def change_choose(key):

    logging.debug("change_choose('{}')".format(key))
    entry = locator.db.get(key)
    print(_format_entry(entry))
    print("What do you want to change?")
    options = {
        'a': 'series',
        'b': 'last_watched',
        'c': 'total',
        'd': 'done',
        'e': 'type',
        'f': 'season',
        'g': 'rating',
        'h': 'airing_days',
        'i': 'ep_notes',
        'j': 'notes',
        'q': 'Quit'}
    order = ('q')
    for i in order:
        print('{} - {}'.format(i, options[i]))

    a = input(globals.PROMPT)
    if a == 'q':
        print("Okay")
        return -1
    else:
        return (change_field, [key, options[a]], {})


def change_field(key, field):
    print('Changing field: {}'.format(field))
    print('Old value: {}'.format(_get_field(field, locator.db.get(key))))

    a = input(globals.PROMPT)
    map = {field: a}
    locator.db.change(key, map)
    print('Done')
    return -1


def _format_entry(entry):
    map = dict((globals.FIELDS[i], entry[i]) for i in range(len(entry)))
    return globals.SEL_ENTRY.format(**map)


def _get_field(field, entry):
    return entry[globals.FIELDS.index(field)]
