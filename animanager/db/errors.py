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


class DatabaseError(Exception):
    """Database error."""


class DatabaseMigrationError(DatabaseError):
    """Database migration error."""


class DatabaseVersionError(DatabaseError):
    """Bad database version."""

    def __init__(self, wanted, found):
        self.wanted = wanted
        self.found = found
        super().__init__('Bad database version: wanted {}, found {}'.format(
            self.wanted, self.found))
