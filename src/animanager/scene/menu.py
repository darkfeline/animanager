import logging
from collections import OrderedDict

from animanager import locator
from animanager.gvars import PROMPT
from animanager.scene import add
from animanager.scene import delete
from animanager.scene import check
from animanager.scene import change

logger = logging.getLogger(__name__)
options = OrderedDict()
options['a'] = ('Add an entry', add.add)
options['m'] = ('Check an entry', check.match)
options['f'] = ('Find an entry', check.find)
options['mc'] = ('Change an entry', change.match)
options['fc'] = ('Find and change an entry', change.find)
options['md'] = ('Delete an entry', delete.match)
options['fd'] = ('Find and delete an entry', delete.find)
options['q'] = ('Quit',)


def main_menu():

    logger.debug('main_menu()')
    print("Welcome to Animanager")
    for key in options:
        print('{} - {}'.format(key, options[key][0]))

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
