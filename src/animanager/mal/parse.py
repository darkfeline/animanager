# Copyright (C) 2015  Allen Li
#
# This file is part of Animanager.
#
# Animanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Animanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Animanager.  If not, see <http://www.gnu.org/licenses/>.

"""
The module contains XML parsing code for MAL.
"""

import logging
from xml.etree import ElementTree

from .preprocess import preprocess

_LOGGER = logging.getLogger(__name__)


def parse(text):
    """Parse XML from MAL.

    Return None if text is empty.

    """
    if not text:
        return None
    _LOGGER.debug(text)
    text = preprocess(text)
    try:
        tree = ElementTree.XML(text)
    except ElementTree.ParseError as err:
        _LOGGER.error('Encountered parse error: %r', err)
        line, col = err.position
        _LOGGER.error('Error at line %s, column %s', line, col)
        text_lines = text.split('\n')
        _LOGGER.error(text_lines[line])
        _LOGGER.error(' ' * (col-1) + '^')
        raise err
    else:
        return tree
