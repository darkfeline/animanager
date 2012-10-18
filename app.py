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
        'q': ('Quit', main_menu)}
    order = ('f', 'q')
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
    return -1


def change_choose():
    return -1


def find():

    logging.debug('find()')
    print('Which entry to find?')

    a = input(PROMPT)
    entries = locator.db.get(a)
    logging.debug(entries)
    if len(entries) == 0:
        print('Cannot find {}'.format(a))
        return -1
    for entry in entries:
        map = dict((FIELDS[i], entry[i]) for i in range(len(entry)))
        logging.debug(map)
        print(ENTRY.format(**map))
        return -1

if __name__ == "__main__":
    main()
