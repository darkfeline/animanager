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

from argparse import Namespace
from cmd import Cmd
from typing import Callable, Optional

import animanager.argparse
import animanager.registry

ExtendedCommand = Callable[[Cmd, Namespace], Optional[bool]]
PlainCommand = Callable[[Cmd, str], Optional[bool]]


class CmdRegistry:

    """Command registry for registering commands."""

    def __init__(self):
        self.do_reg = animanager.registry.Registry('do_')
        self.do_reverse = dict()
        self.help_reg = animanager.registry.Registry('help_')

    def register_command(
            self, name: str, parser: animanager.argparse.ArgumentParser,
    ) -> Callable[[ExtendedCommand], PlainCommand]:
        """Decorator for registering commands."""
        def decorate(func: ExtendedCommand) -> PlainCommand:
            # Add argument parsing.
            new_func = parser.parsing(func)  # type: PlainCommand
            # Register do_*.
            self.do_reg[name] = new_func
            self.do_reverse[new_func] = name
            # Register help_*.
            if not parser.description and func.__doc__:
                parser.description = func.__doc__
            def help_func(self: Cmd) -> None:
                parser.print_help()
            self.help_reg[name] = help_func
            return new_func
        return decorate

    def register_alias(
            self, alias: str,
    ) -> Callable[[PlainCommand], PlainCommand]:
        """Decorator for registering command alias."""
        def decorate(func: PlainCommand) -> PlainCommand:
            self.do_reg[alias] = func
            original_name = self.do_reverse[func]
            help_string = 'Alias for {}'.format(original_name)
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
