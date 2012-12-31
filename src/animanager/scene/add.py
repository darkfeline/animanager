import logging

from animanager import globals
from animanager import locator

logger = logging.getLogger(__name__)


def add():

    logger.debug('add.add()')
    print('Name of entry to add')

    a = input(globals.PROMPT)
    try:
        locator.db.add({'series': a})
    except Exception as e:
        raise e
    else:
        print('Added {}'.format(a))
    return -2
