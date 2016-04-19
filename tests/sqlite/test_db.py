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

import hypothesis
from hypothesis import strategies

from animanager.sqlite.db import SQLiteDB

# pylint doesn't understand hypothesis
# pylint: disable=no-value-for-parameter


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.db = SQLiteDB(':memory:')

    @hypothesis.given(strategies.integers(-2**31, 2**31-1))
    def test_set_version(self, ver):
        self.db.set_version(ver)
        new_ver = self.db.get_version()
        self.assertEqual(ver, new_ver)
