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

"""General XML tools."""

import xml.etree.ElementTree as ET


class XMLTree:

    """XML ElementTree wrapper class.

    Be careful, `tree` should be an :class:`xml.etree.ElementTree.ElementTree`
    instance.

    :param xml.etree.ElementTree.ElementTree tree: XML tree to wrap

    .. attribute:: tree (ElementTree)

       Wrapped ElementTree.

    .. attribute:: root (Element)

       Wrapped root Element.

    """

    def __init__(self, tree: ET.ElementTree) -> None:
        if not isinstance(tree, ET.ElementTree):
            raise TypeError('Not an ElementTree object.')
        self.tree = tree
        self.root = tree.getroot()

    @classmethod
    def parse(cls, file: str) -> 'XMLTree':
        """Create instance from an XML file.

        :param str file: XML file path

        """
        return cls(ET.parse(file))

    @classmethod
    def fromstring(cls, text: str) -> 'XMLTree':
        """Create instance from an XML string.

        :param str text: XML string

        """
        return cls(ET.ElementTree(ET.fromstring(text)))

    def write(self, file: str) -> None:
        """Write XML to a file.

        :param str file: file path

        """
        self.tree.write(file)
