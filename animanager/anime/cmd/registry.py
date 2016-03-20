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
            self.do_funcs[name] = func
            self.do_funcs_reverse[func] = name
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

    def add_commands(self, cmd):
        """Add registered commands to Cmd instance."""
        for name, func in self.do_funcs.items():
            setattr(cmd, 'do_' + name, func)
        for name, func in self.help_funcs.items():
            setattr(cmd, 'help_' + name, func)
