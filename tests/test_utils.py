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
from unittest.mock import Mock

from animanager.utils import CachedProperty


class CachedPropertyTestCase(unittest.TestCase):

    """Test CachedProperty"""

    def setUp(self):
        self.func = Mock([])
        self.prop = CachedProperty(self.func)
        self.type = type('Foo', (), {'foo': self.prop})
        self.obj = self.type()

    def test_cached_property(self):
        """Test CachedProperty get and delete."""
        # First access
        foo = self.obj.foo
        self.assertIs(foo, self.func.return_value)
        self.func.assert_called_once_with(self.obj)

        # Second access should hit cache.
        self.func.reset_mock()
        foo = self.obj.foo
        self.assertIs(foo, self.func.return_value)
        self.func.assert_not_called()

        # Clear cache, third access.
        self.func.reset_mock()
        del self.obj.foo
        foo = self.obj.foo
        self.assertIs(foo, self.func.return_value)
        self.func.assert_called_once_with(self.obj)

    def test_cached_property_set(self):
        """Test CachedProperty set."""
        with self.assertRaises(AttributeError):
            self.obj.foo = 2
