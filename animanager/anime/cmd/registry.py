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


class Registry:

    """Command registry for registering commands."""

    def __init__(self):
        self.commands = dict()

    def __setitem__(self, attribute, value):
        self.commands[attribute] = value

    def register(self, name):
        """Decorator for registering commands."""
        def decorate(func):
            self[name] = func
            return func
        return decorate

    def add_commands(self, cmd):
        """Add registered commands to Cmd instance."""
        for name, func in self.commands.items():
            setattr(cmd, name, func)
