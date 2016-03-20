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

from animanager.db import migrations


class GoodMigrationsTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = migrations.MigrationManager()
        self.m1 = migrations.make_migration(0, 1, lambda: None)
        self.m2 = migrations.make_migration(1, 2, lambda: None)

    def test_register(self):
        self.manager.register(self.m1())
        self.manager.register(self.m2())
        self.assertEqual(self.manager.current_version, 2)

    def test_register_disjoint(self):
        with self.assertRaises(ValueError):
            self.manager.register(self.m2())

    def test_register_migration_class(self):
        with self.assertRaises(TypeError):
            self.manager.register(self.m1)
