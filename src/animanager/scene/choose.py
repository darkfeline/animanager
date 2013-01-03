import logging

from animanager import locator
from animanager import gvars

logger = logging.getLogger(__name__)


def choose_entry(entries, next):

    logger.debug('choose_entry(%s, %s)', entries, next)
    for i, entry in enumerate(entries):
        print('{} - {}'.format(i, entry[0]))
    print('q - quit')
    print()
    print('Select an entry.')

    a = input(gvars.PROMPT)
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
            locator.stack.add((next, [key], {}))
