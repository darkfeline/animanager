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

    """Class for registering methods for a class."""

    def __init__(self, prefix=''):
        self.prefix = prefix
        self.methods = dict()

    def __getitem__(self, name):
        return self.methods[name]

    def __setitem__(self, name, func):
        self.methods[name] = func

    def __contains__(self, name):
        return name in self.methods

    def register(self, name):
        """Decorator for registering commands."""
        def decorate(func):
            self[name] = func
            return func
        return decorate

    @staticmethod
    def add_method(obj, attr, value):
        if hasattr(obj, attr):
            raise DuplicateAttributeError(obj, attr)
        setattr(obj, attr, value)

    def add_methods(self, cls):
        """Add registered commands to Cmd instance."""
        for name, func in self.methods.items():
            self.add_method(cls, self.prefix + name, func)


class RegistryError(Exception):
    pass


class DuplicateAttributeError(RegistryError):

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr
        super().__init__('{} already has attribute {}'.format(obj, attr))
