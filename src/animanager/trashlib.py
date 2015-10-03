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

"""This module defines a trash function for reversibly deleting files."""

import os
import logging

_TRASH_DIR = 'trash'
_LOGGER = logging.getLogger(__name__)


def trash(file):
    """Trash file.

    Move file to a designated trash directory.

    """
    _LOGGER.info('Trashing %s', file)
    if not os.path.exists(_TRASH_DIR):
        os.mkdir(_TRASH_DIR)
    os.rename(file, os.path.join(_TRASH_DIR, os.path.basename(file)))
