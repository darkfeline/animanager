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

"""Tools for managing temporary cache tables in a SQLite database."""


from collections import namedtuple


class CacheTableManager:

    """CacheTable manager.

    Instances of this class manage cache table setup and cleanup.
    """

    def __init__(self, conn, table_specs: 'Iterable[CacheTableSpec]'):
        self._conn = conn
        self._table_specs = tuple(table_specs)

    def setup(self):
        """Setup cache tables."""
        for table_spec in self._table_specs:
            with self._conn:
                table_spec.setup(self._conn)

    def teardown(self):
        """Cleanup cache tables."""
        for table_spec in reversed(self._table_specs):
            with self._conn:
                table_spec.teardown(self._conn)


CacheTableSpec = namedtuple('CacheTableSpec', 'setup,teardown')
