
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
import doctest

from animanager.anime import cmd

from . import parse_aid

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(cmd))
    suite.addTests(loader.loadTestsFromModule(parse_aid))
    return suite
