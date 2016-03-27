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


class MetaCommandError(Exception):
    """Error in meta command definition."""

    def __init__(self, message=''):
        if not message:
            message = 'Error in meta command definition'
        super().__init__(message)


class DanglingAliasError(MetaCommandError):
    """Alias missing its command in command mixin class."""

    def __init__(self, alias, full_name):
        self.alias = alias
        self.full_name = full_name
        message = 'Alias do_{} missing its command do_{}'.format(
            alias, full_name)
        super().__init__(message)


class CommandExit(Exception):
    """This is used to exit a command in lieu of sys.exit()"""
