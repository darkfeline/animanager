# Copyright (C) 2016  Allen Li
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

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods


class Request(ABC):

    """API request abstract class."""

    @abstractmethod
    def open(self):
        """Perform request."""
        logger.debug('Opened request %s', self)


class Response(ABC):

    @abstractmethod
    def content(self):
        """Get response content."""
        return ''
