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

"""General XML tools."""

import xml.etree.ElementTree as ET


class XMLTree:

    """XML ElementTree wrapper class.

    Be careful, tree should be an xml.etree.ElementTree.ElementTree
    instance.
    """

    def __init__(self, tree: ET.ElementTree):
        if not isinstance(tree, ET.ElementTree):
            raise TypeError('Not an ElementTree object.')
        self.tree = tree
        self.root = tree.getroot()

    @classmethod
    def parse(cls: 'A', file: str) -> 'A':
        """Create instance from an XML file."""
        return cls(ET.parse(file))

    @classmethod
    def fromstring(cls: 'A', text: str) -> 'A':
        """Create instance from an XML string."""
        return cls(ET.ElementTree(ET.fromstring(text)))

    def write(self, file: str):
        """Write XML to a file."""
        self.tree.write(file)
