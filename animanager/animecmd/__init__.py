# Copyright (C) 2016-2017  Allen Li
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

import logging
import os
import shlex

from dataclasses import dataclass
import apsw

import mir.cp

from animanager.anidb import TitleSearcher
from animanager.cmd import Command
from animanager.cmd import ParseExit
from animanager.cmd.results import AIDParseError, AIDResults, AIDResultsManager
from animanager.cmdlib import CmdExit
from animanager import commands
from animanager.db import cachetable, query
from animanager.files import FilePicker, Rule

from . import (
    reset, search, show, unregister,
)

logger = logging.getLogger(__name__)


class AnimeCmd:

    prompt = 'A> '
    commands = {
        '?': commands.help,
        'a': commands.add,
        'add': commands.add,
        'addrule': commands.addrule,
        'as': commands.asearch,
        'asearch': commands.asearch,
        'deleterule': commands.deleterule,
        'gpl': commands.gpl,
        'help': commands.help,
        'purgecache': commands.purgecache,
        'q': commands.quit,
        'quit': commands.quit,
        'r': reset.command,
        'reg': commands.register,
        'register': commands.register,
        'reset': reset.command,
        'rules': commands.rules,
        's': search.command,
        'search': search.command,
        'sh': show.command,
        'show': show.command,
        'u': commands.update,
        'unreg': unregister.command,
        'unregister': unregister.command,
        'update': commands.update,
        'w': commands.watch,
        'watch': commands.watch,
    }
    safe_exceptions = set([AIDParseError])

    def __init__(self, config):
        self.state = State()
        self.last_cmd = []

        self.config = config
        self.titles = TitleSearcher(config['anime'].getpath('anidb_cache'))
        dbfile = config['anime'].getpath('database')
        self.conn = self.db = _connect(dbfile)

        self.cache_manager = cachetable.make_manager(self.db)
        self.cache_manager.setup()

        self.results = AIDResultsManager({
            'db': AIDResults([
                'Title', 'Type', 'Episodes', 'Complete', 'Available',
            ]),
            'anidb': AIDResults(['Title']),
        })

    def cmdloop(self):
        """Start CLI REPL."""
        while True:
            cmdline = input(self.prompt)
            tokens = shlex.split(cmdline)
            if not tokens:
                if self.last_cmd:
                    tokens = self.last_cmd
                else:
                    print('No previous command.')
                    continue
            if tokens[0] not in self.commands:
                print('Invalid command')
                continue
            command = self.commands[tokens[0]]
            self.last_cmd = tokens
            try:
                if isinstance(command, Command):
                    if command(self, *tokens[1:]):
                        break
                else:
                    if command(self, tokens):
                        break
            except ParseExit:
                continue
            except CmdExit:
                continue
            except Exception as e:
                if e not in self.safe_exceptions:
                    logger.exception('Error!')

    @mir.cp.NonDataCachedProperty
    def file_picker(self) -> FilePicker:
        """Cached file picker property."""
        return FilePicker(
            Rule(rule.regexp, rule.priority)
            for rule in query.files.get_priority_rules(self.db))


@dataclass
class State:
    ...


def _connect(dbfile: 'PathLike') -> apsw.Connection:
    """Connect to SQLite database file."""
    conn = apsw.Connection(os.fspath(dbfile))
    _set_foreign_keys(conn, 1)
    assert _get_foreign_keys(conn) == 1
    return conn


def _get_foreign_keys(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys')
    return cur.fetchone()[0]


def _set_foreign_keys(conn, value: int):
    cur = conn.cursor()
    cur.execute(f'PRAGMA foreign_keys={value:d}')
