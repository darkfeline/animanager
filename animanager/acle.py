# Copyright (C) 2016, 2017  Allen Li
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

"""This package contains tools for constructing custom Cmd, command line
interface classes.

"""

import argparse
import asyncio
import functools

from mir.acle import base
from mir.acle import handlers

import animanager

from animanager.cmd.argparse import ArgumentParser
from animanager.cmd.utils import compile_re_query


_INTRO = f'''\
Animanager {animanager.__version__}
Copyright (C) 2015-2017  Allen Li

This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
This is free software, and you are welcome to redistribute it
under certain conditions; type "gpl c" for details.'''


def start_command_line(cmd, loop=None):
    if loop is None:  # pragma: no cover
        loop = asyncio.get_event_loop()
    prompt = Prompt()
    handler = _make_handler(prompt, cmd)
    base.start_command_line(handler, pre_hook=prompt.print, loop=loop)


def _make_handler(prompt, cmd):
    handler = handlers.ShellHandler()
    state = CmdState(prompt, cmd)
    # handler.set_default_handler(handler)
    handler.add_command('asearch', functools.partial(_asearch, state))
    return handler


async def _asearch(state, args):
    """Search AniDB."""
    parser = ArgumentParser(prog='asearch')
    parser.add_argument('query', nargs=argparse.REMAINDER)
    args = parser.parse_args(args)
    if not args.query:
        print('Must supply query.')
        return
    search_query = compile_re_query(args.query)
    results = state.cmd.titles.search(search_query)
    results = [(anime.aid, anime.main_title) for anime in results]
    state.cmd.results['anidb'].set(results)
    state.cmd.results['anidb'].print()


class CmdState:

    def __init__(self, prompt, cmd):
        self.last_command = None
        self._prompt = prompt
        self.cmd = cmd

    def print_prompt(self):
        self._prompt.print()


class Prompt:

    prompt = 'A> '

    def print(self):
        print(self.prompt, end='', flush=True)
