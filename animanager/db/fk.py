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

from animanager.db import DatabaseError

from .migrations import MigrationManager as PlainMigrationManager
from .sqlite import SQLiteDB


class ForeignKeyMixin(SQLiteDB):

    """Enables SQLite foreign key support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cur = self.cnx.cursor()
        cur.execute('PRAGMA foreign_keys = 1')
        cur.execute('PRAGMA foreign_keys')
        if cur.fetchone()[0] != 1:
            raise DatabaseError('Foreign keys are not supported.')


class MigrationManager(PlainMigrationManager):

    """Migration extended with foreign key handling."""

    def migrate_single(self, cnx, version):
        cur = cnx.cursor()
        cur.execute('PRAGMA foreign_keys = 0')
        with cnx:
            version = super().migrate_single(cnx, version)
            cur.execute('PRAGMA foreign_key_check')
        cur.execute('PRAGMA foreign_keys = 1')
        return version
