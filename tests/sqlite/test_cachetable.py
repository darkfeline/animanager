# Copyright (C) 2016-2017  Allen Li
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

import unittest
from unittest import mock
from unittest.mock import Mock

from apsw import Connection

from animanager.sqlite.cachetable import CacheTableSpec
from animanager.sqlite.cachetable import CacheTableManager


class CacheTableTestCase(unittest.TestCase):

    def setUp(self):
        self.db = mock.create_autospec(Connection, instance=True)
        self.setup = Mock([])
        self.teardown = Mock([])
        self.table = table = CacheTableSpec(self.setup, self.teardown)

        self.manager = CacheTableManager(self.db, [table])

    def test_setup(self):
        self.manager.setup()
        self.setup.assert_called_once_with(self.db)
        self.teardown.assert_not_called()

    def test_cleanup(self):
        self.manager.teardown()
        self.setup.assert_not_called()
        self.teardown.assert_called_once_with(self.db)
