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

from animanager.anime.cmd import AnimeCmd
from animanager.anime.cmd.results import AIDSearchResults


class FakeAnimeCmd:

    def __init__(self, results, aresults):
        self.results = AIDSearchResults(['aid'])
        self.results.set(results)
        self.aresults = AIDSearchResults(['aid'])
        self.aresults.set(aresults)

    parse_aid = AnimeCmd.parse_aid


class ParseAIDTestCase(unittest.TestCase):

    def setUp(self):
        self.cmd = FakeAnimeCmd(
            [(1, 'Madoka'), (2, 'Madoka'), (3, 'Madoka')],
            [(4, 'Madoka'), (5, 'Madoka'), (6, 'Madoka')])
        self.parse_aid = self.cmd.parse_aid

    def test_explicit_aid(self):
        self.assertEqual(self.parse_aid('aid:12345'), 12345)

    def test_explicit_results(self):
        self.assertEqual(self.parse_aid('#:2'), 2)

    def test_explicit_aresults(self):
        self.assertEqual(self.parse_aid('a#:2'), 5)

    def test_implicit_results(self):
        self.assertEqual(self.parse_aid('3', False), 3)

    def test_implicit_aresults(self):
        self.assertEqual(self.parse_aid('3', True), 6)
