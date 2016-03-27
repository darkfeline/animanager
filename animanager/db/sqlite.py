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

import apsw

from .abc import BaseDatabase


class SQLiteDB(BaseDatabase):

    """SQLite database.

    Provides minimum functionality for a SQLite connection.

    SQLiteDB mixins that extend __init__() should call super().__init__()
    before running their own code, especially if they need access to the SQLite
    connection.  Mixins should therefore be included in reverse order:

        class Foo(SpamMixin, EggsMixin, SQLiteDB):

    This will run __init__() in order: SQLiteDB, EggsMixin, SpamMixin

    """

    def __init__(self, *args, **kwargs):
        self.connect(*args, **kwargs)

    def connect(self, *args, **kwargs):
        # pylint: disable=no-member
        self.cnx = apsw.Connection(*args, **kwargs)

    def close(self):
        self.cnx.close()
