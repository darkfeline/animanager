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
        self.do_funcs = dict()
        self.do_funcs_reverse = dict()
        self.help_funcs = dict()

    def register_do(self, name):
        """Decorator for registering commands."""
        def decorate(func):
            # Register do_*.
            self.do_funcs[name] = func
            self.do_funcs_reverse[func] = name

            # Register help_* if we don't have one yet.
            if name not in self.help_funcs:
                def help_func(self):
                    print(func.__doc__)
                self.help_funcs[name] = help_func
            return func
        return decorate

    def register_help(self, name):
        """Decorator for registering command help."""
        def decorate(func):
            self.help_funcs[name] = func
            return func
        return decorate

    def register_alias(self, alias):
        """Decorator for registering command alias."""
        def decorate(func):
            original = self.do_funcs_reverse[func]
            self.do_funcs[alias] = self.do_funcs[original]
            help_string = 'Alias for {}'.format(original)
            def help_func(self):
                print(help_string)
            self.help_funcs[alias] = help_func
            return func
        return decorate

    @staticmethod
    def setattr(obj, attr, value):
        if hasattr(obj, attr):
            raise DuplicateRegisterError(obj, attr)
        setattr(obj, attr, value)

    def add_commands(self, cmd):
        """Add registered commands to Cmd instance."""
        for name, func in self.do_funcs.items():
            self.setattr(cmd, 'do_' + name, func)
        for name, func in self.help_funcs.items():
            self.setattr(cmd, 'help_' + name, func)


class RegistryError(Exception):
    pass


class DuplicateRegisterError(ValueError, RegistryError):

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr
        super().__init__('{} already has attribute {}'.format(obj, attr))
