# Copyright (C) 2015-2016  Allen Li
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

_LOGGER = logging.getLogger(__name__)


def trashdir(config):
    """Return path of trash directory."""
    dir = config['watch'].getpath('directory')
    return os.path.join(dir, 'trash')


def trash(config, file):
    """Trash file.

    Move file to a designated trash directory.

    """
    _LOGGER.info('Trashing %s', file)
    td = trashdir(config)
    if not os.path.exists(td):
        os.mkdir(td)
    os.rename(file, os.path.join(td, os.path.basename(file)))
