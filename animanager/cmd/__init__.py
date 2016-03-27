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

"""Animanager's command line interface."""

import functools
import shlex
from argparse import ArgumentParser, Namespace
from cmd import Cmd
from typing import Callable, Optional

ExtendedCommand = Callable[[Cmd, Namespace], Optional[bool]]
PlainCommand = Callable[[Cmd, str], Optional[bool]]
HelpCommand = Callable[[Cmd], None]


class CmdMixinMeta(type):

    """Metaclass for making command mixing classes."""

    def __new__(mcs, name, parents, dct):
        # Set up commands.
        dct_items = list(dct.items())
        for attr, obj in dct_items:
            # Set up command.
            if attr.startswith('do_'):
                cmd_name = attr[3:]
                command = obj

                # Get parser for this command.
                try:
                    parser = dct['parser_' + cmd_name]
                except KeyError:
                    raise MissingParserError(cmd_name)
                # Add command name as parser prog name.
                parser.prog = cmd_name
                # Add command docstring as default parser description.
                if not parser.description:
                    parser.description = command.__doc__

                # Wrap command with argument parsing.
                plain_command = mcs._with_parsing(command, parser)
                dct['do_' + cmd_name] = plain_command
                # Add command help.
                dct['help_' + cmd_name] = mcs._command_help(parser)

        # Set up aliases.
        for attr, obj in dct_items:
            if attr.startswith('alias_'):
                alias = attr[6:]
                command = obj  # type: str
                dct['do_' + alias] = mcs._alias_do(alias, command)
                dct['help_' + alias] = mcs._alias_help(command)
        return super().__new__(mcs, name, parents, dct)

    @staticmethod
    def _with_parsing(
            command: ExtendedCommand,
            parser: ArgumentParser,
    ) -> PlainCommand:
        """Wrap an ExtendedCommand with argument parsing."""
        @functools.wraps(command)
        def plain_command(self, arg):
            # pylint: disable=missing-docstring
            args = parser.parse_args(shlex.split(arg))
            return command(self, args)
        return plain_command

    @staticmethod
    def _command_help(parser: ArgumentParser) -> HelpCommand:
        """Make a command help_* method."""
        def command_help(self):
            # pylint: disable=missing-docstring,unused-argument
            parser.print_help()
        return command_help

    @staticmethod
    def _alias_do(alias: str, command: str) -> PlainCommand:
        """Make an alias command do_* method."""
        command = 'do_' + command
        def alias_do(self, args):
            # pylint: disable=missing-docstring
            try:
                method = getattr(self, command)
            except AttributeError:
                raise DanglingAliasError(alias, command)
            return method(args)
        return alias_do

    @staticmethod
    def _alias_help(command_name: str) -> HelpCommand:
        """Make an alias command help_* method."""
        help_msg = 'Alias for {}'.format(command_name)
        def alias_help(self):
            # pylint: disable=missing-docstring,unused-argument
            print(help_msg)
        return alias_help


class CmdMeta(CmdMixinMeta):

    """Metaclass for Cmd classes that use command mixins.

    This satisfies Python's metaclass rules and overrides CmdMixinMeta.

    """

    def __new__(mcs, name, parents, dct):
        return type.__new__(mcs, name, parents, dct)


class MetaCommandError(Exception):
    """Error in meta command definition."""

    def __init__(self, message=''):
        if not message:
            message = 'Error in meta command definition'
        super().__init__(message)


class MissingParserError(Exception):
    """Command missing its parser in command mixin class."""

    def __init__(self, command):
        self.command = command
        message = 'Command do_{} missing its parser parser_{}'.format(
            command, command)
        super().__init__(message)


class DanglingAliasError(Exception):
    """Alias missing its command in command mixin class."""

    def __init__(self, alias, full_name):
        self.alias = alias
        self.full_name = full_name
        message = 'Alias do_{} missing its command do_{}'.format(
            alias, full_name)
        super().__init__(message)
