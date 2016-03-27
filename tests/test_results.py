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

from animanager.cmd.results import AIDResults, AIDResultsManager


class ParseAIDTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = AIDResultsManager()
        results = AIDResults(['Title'])
        results.set([(1, 'Madoka'), (2, 'Madoka'), (3, 'Madoka')])
        self.manager['foo'] = results
        results = AIDResults(['Title'])
        results.set([(4, 'Madoka'), (5, 'Madoka'), (6, 'Madoka')])
        self.manager['bar'] = results

    def test_explicit_aid(self):
        self.assertEqual(self.manager.parse_aid('aid:12345', 'foo'), 12345)

    def test_explicit_key(self):
        self.assertEqual(self.manager.parse_aid('#foo:2', 'foo'), 2)

    def test_implicit_key(self):
        self.assertEqual(self.manager.parse_aid('3', 'bar'), 6)

    def test_invalid_key_syntax(self):
        with self.assertRaises(ValueError):
            self.manager.parse_aid('#:3', 'foo')

    def test_invalid_key(self):
        with self.assertRaises(KeyError):
            self.manager.parse_aid('#spam:3', 'foo')

    def test_invalid_number(self):
        with self.assertRaises(IndexError):
            self.manager.parse_aid('#foo:5', 'foo')
