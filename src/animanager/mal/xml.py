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
import re
from xml.etree import ElementTree

from .. import xmllib

_LOGGER = logging.getLogger(__name__)
DOCTYPE = '<!DOCTYPE data PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" ' + \
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'


def parse(text):
    """Parse XML from MAL.

    Return None if text is empty.

    """
    if not text:
        return None
    _LOGGER.debug(text)

    # Split up input text to do some MAL-specific preprocessing.
    text = text.split('\n')
    # Hack for MAL behavior.
    # MAL doesn't return proper XML if there are no results.
    if text[0] == 'No results':
        return None
    # Insert propert doctype since MAL doesn't have it.
    text[1:1] = [DOCTYPE]
    text = '\n'.join(text)

    text = xmllib.preprocess(text)
    parser = ElementTree.XMLParser()
    try:
        tree = ElementTree.XML(text, parser=parser)
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
