import logging

from globals import PROMPT
from scene import find
from scene import change


def main_menu():

    logging.debug('main_menu()')
    print("Welcome to Animanager")
    options = {
        'f': ('Find an entry', find.find),
        'c': ('Change an entry', change.change_find),
        'q': ('Quit',)}
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
