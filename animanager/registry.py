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

# pylint: disable=unsubscriptable-object


class Registry:

    """Class for registering methods for a class."""

    def __init__(self, prefix=''):
        self.prefix = prefix
        self.methods = dict()

    def __getattr__(self, name):
        return self.methods[name]

    def __setattr__(self, name, func):
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


class CmdRegistry:

    """Command registry for registering commands."""

    def __init__(self):
        self.do_reg = Registry('do_')
        self.do_reverse = dict()
        self.help_reg = Registry('help_')

    def register_do(self, name):
        """Decorator for registering commands."""
        def decorate(func):
            self.do_reg[name] = func
            self.do_reverse[func] = name
            if name not in self.help_reg:
                def help_func(self):
                    # pylint: disable=unused-argument
                    print(func.__doc__)
                self.help_reg[name] = help_func
            return func
        return decorate

    def register_help(self, name):
        """Decorator for registering command help."""
        return self.help_reg.register(name)

    def register_alias(self, alias):
        """Decorator for registering command alias."""
        def decorate(func):
            self.do_reg[alias] = func
            original = self.do_reverse[func]
            help_string = 'Alias for {}'.format(original)
            def help_func(self):
                # pylint: disable=unused-argument
                print(help_string)
            self.help_reg[alias] = help_func
            return func
        return decorate

    def add_commands(self, cmd):
        """Add registered commands to Cmd instance."""
        self.do_reg.add_methods(cmd)
        self.help_reg.add_methods(cmd)


class RegistryError(Exception):
    pass


class DuplicateAttributeError(RegistryError):

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr
        super().__init__('{} already has attribute {}'.format(obj, attr))
