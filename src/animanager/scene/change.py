import logging

from animanager import gvars
from animanager import locator
from animanager.scene import choose

logger = logging.getLogger(__name__)


def match():

    logger.debug('match()')
    print('Which entry to change?')

    a = input(gvars.PROMPT)
    entry = locator.db.get(a)
    if entry is None:
        print('No match for {}'.format(a))
        return -2
    else:
        locator.stack.add((choose, [a], {}))


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
        locator.stack.add((choose.choose_entry, [entries, choose_field], {}))


def choose_field(key):

    logger.debug("choose_field('{}')".format(key))
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

    a = input(gvars.PROMPT)
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

    logger.debug('change_field({}, {})'.format(key, field))
    print('Changing field: {}'.format(field))
    print('Old value: {}'.format(_get_field(field, locator.db.get(key))))

    a = input(gvars.PROMPT)
    if not a:
        print('Empty input')
        print('Cancel (or set to null)? [Y/n/c(lear)]')
        a = input(gvars.PROMPT)
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
    map = dict((gvars.FIELDS[i], entry[i]) for i in range(len(entry)))
    return gvars.SEL_ENTRY.format(**map)


def _get_field(field, entry):
    return entry[gvars.FIELDS.index(field)]
