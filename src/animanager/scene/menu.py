import logging

from animanager import locator
from animanager.globals import PROMPT
from animanager.scene import find
from animanager.scene import change

options = {
    'f': ('Find an entry', find.find),
    's': ('Search for an entry', find.search),
    'c': ('Change an entry', change.find),
    'd': ('Search and change', change.search),
    'q': ('Quit',)}
order = ('f', 's', 'c', 'd', 'q')


def main_menu():

    logging.debug('main_menu()')
    print("Welcome to Animanager")
    for i in order:
        print('{} - {}'.format(i, options[i][0]))

    a = input(PROMPT)
    if a == 'q':
        print("Bye")
        return -1
    try:
        x = (options[a][1], [], {})
    except KeyError:
        print("{} is not a valid option".format(a))
        return
    else:
        locator.stack.push(x)
