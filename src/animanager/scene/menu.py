import logging
from collections import OrderedDict

from animanager import locator
from animanager.globals import PROMPT
from animanager.scene import add
from animanager.scene import find
from animanager.scene import change

logger = logging.getLogger(__name__)
options = OrderedDict()
options['a'] = ('Add an entry', add.add)
options['f'] = ('Find an entry', find.find)
options['s'] = ('Search for an entry', find.search)
options['fc'] = ('Find and change an entry', change.find)
options['sc'] = ('Search for and change an entry', change.search)
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
