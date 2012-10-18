#!/usr/bin/env python3

import logging

import db
import locator

FIELDS = ('series', 'last_watched', 'total', 'done', 'type', 'season',
          'rating', 'airing_days', 'ep_notes', 'notes')
ENTRY = """Series: {series}
Last: {last_watched}
Total: {total}
Done: {done}
Type: {type}
Season: {season}
Rating: {rating}
Airing Days: {airing_days}
Ep. Notes: {ep_notes}
Notes: {notes}

"""
SEL_ENTRY = """a - Series: {series}
b - Last: {last_watched}
c - Total: {total}
d - Done: {done}
e - Type: {type}
f - Season: {season}
g - Rating: {rating}
h - Airing Days: {airing_days}
i - Ep. Notes: {ep_notes}
j - Notes: {notes}

"""
PROMPT = ">>> "

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def main():
    """
    Functions:
    Return a tuple with first value callable to add to stack
        (function, args, kwargs)
    Return -1 to pop
    Return None to repeat

    """
    locator.db = db.AnimeDB()
    stack = []
    stack.append((main_menu, [], {}))
    while len(stack) > 0:
        func, args, kwargs = stack[-1]
        a = func(*args, **kwargs)
        if a is None:
            continue
        elif isinstance(a, tuple) and hasattr(a[0], '__call__'):
            stack.append(a)
        elif a == -1:
            stack.pop()


def main_menu():

    logging.debug('main_menu()')
    print("Welcome to Animanager")
    options = {
        'f': ('Find an entry', find),
        'c': ('Change an entry', change_find),
        'q': ('Quit', main_menu)}
    order = ('f', 'c', 'q')
    for i in order:
        print('{} - {}'.format(i, options[i][0]))

    a = input(PROMPT)
    if a == 'q':
        print("Bye")
        return -1
    try:
        return (options[a][1], [], {})
    except KeyError:
        print("{} is not a valid option".format(a))
        return


def change_find():

    logging.debug('change_find()')
    print('Which entry to change?')

    a = input(PROMPT)
    entry = locator.db.get(a)
    if entry is None:
        print('Cannot find {}'.format(a))
        return -1
    else:
        return (change_choose, [a], {})


def change_choose(key):

    logging.debug("change_choose('{}')".format(key))
    entry = locator.db.get(key)
    print(format_entry(entry))
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

    a = input(PROMPT)
    if a == 'q':
        print("Okay")
        return -1
    else:
        return (change_field, [key, options[a]], {})


def change_field(key, field):
    return -1


def find():

    logging.debug('find()')
    print('Which entry to find?')

    a = input(PROMPT)
    entry = locator.db.get(a)
    logging.debug(entry)
    if entry is None:
        print('Cannot find {}'.format(a))
        return -1
    else:
        print(format_entry(entry))
        return -1


def format_entry(entry):
    map = dict((FIELDS[i], entry[i]) for i in range(len(entry)))
    return ENTRY.format(**map)


def get_field(field, entry):
    return entry[FIELDS.index(field)]

if __name__ == "__main__":
    main()
