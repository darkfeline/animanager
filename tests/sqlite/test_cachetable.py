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

import unittest
from unittest.mock import MagicMock

from animanager.sqlite.cachetable import CacheTable, CacheTableManager


class CacheTableTestCase(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.table = table = CacheTable()
        self.setup = MagicMock()
        self.cleanup = MagicMock()

        table.setup(self.setup)
        table.cleanup(self.cleanup)

        self.manager = CacheTableManager(self.db, [table])

    def test_setup(self):
        self.manager.setup()
        self.setup.assert_called_once_with(self.db)
        self.cleanup.assert_not_called()

    def test_cleanup(self):
        self.manager.cleanup()
        self.setup.assert_not_called()
        self.cleanup.assert_called_once_with(self.db)
