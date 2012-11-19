import logging

from animanager import globals
from animanager import locator


def find():

    logging.debug('change.find()')
    print('Which entry to change?')

    a = input(globals.PROMPT)
    entry = locator.db.get(a)
    if entry is None:
        print('Cannot find {}'.format(a))
        return -2
    else:
        locator.stack.add((choose, [a], {}))


def search():

    logging.debug('change.search()')
    print('Search for what?')

    a = input(globals.PROMPT)
    entries = locator.db.search(a)
    logging.debug('Found {}'.format(entries))

    if not entries:
        print('Cannot find {}'.format(a))
        return -2
    else:
        locator.stack.add((search_choose, [entries], {}))


def search_choose(entries):

    logging.debug('change.search_choose({})'.format(entries))
    for i, entry in enumerate(entries):
        print('{} - {}'.format(i, entry[0]))
    print('q - quit')
    print()
    print('Which entry to change?')

    a = input(globals.PROMPT)
    if a == 'q':
        print("Okay")
        return -2
    else:
        try:
            key = entries[int(a)][0]
        except IndexError:
            print('Bad input {}'.format(a))
            return
        else:
            locator.stack.add((choose, [key], {}))


def choose(key):

    logging.debug("change.choose('{}')".format(key))
    entry = locator.db.get(key)
    print(_format_entry(entry))
    print('q - Quit')
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
        'j': 'notes'}

    a = input(globals.PROMPT)
    if a == 'q':
        print("Okay")
        return -2
    else:
        try:
            b = (change_field, [key, options[a]], {})
        except KeyError:
            print("Bad input {}".format(a))
            return
        else:
            locator.stack.push(b)


def change_field(key, field):

    logging.debug('change_field({}, {})'.format(key, field))
    print('Changing field: {}'.format(field))
    print('Old value: {}'.format(_get_field(field, locator.db.get(key))))

    a = input(globals.PROMPT)
    if not a:
        print('Empty input')
        print('Cancel (or set to null)? [Y/n/c(lear)]')
        a = input(globals.PROMPT)
        if a == 'n':
            return
        elif a == 'c':
            print('Setting to null')
            a = None
        else:
            print('Okay')
            return -1

    map = {field: a}
    locator.db.change(key, map)
    print('Done')
    return -2


def _format_entry(entry):
    map = dict((globals.FIELDS[i], entry[i]) for i in range(len(entry)))
    return globals.SEL_ENTRY.format(**map)


def _get_field(field, entry):
    return entry[globals.FIELDS.index(field)]
