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
from animanager.db import cachetable, query
from animanager.files import FilePicker, Rule

from . import (
    add, addrule, asearch, bump, deleterule, gpl, helpcmd, purgecache,
    quitcmd, register, reset, rules, search, show, unregister, update, watch,
)

logger = logging.getLogger(__name__)


class AnimeCmd:

    prompt = 'A> '
    commands = {
        '?': helpcmd.command,
        'a': add.command,
        'add': add.command,
        'addrule': addrule.command,
        'as': asearch.command,
        'asearch': asearch.command,
        'b': bump.command,
        'bump': bump.command,
        'deleterule': deleterule.command,
        'gpl': gpl.command,
        'help': helpcmd.command,
        'purgecache': purgecache.command,
        'q': quitcmd.command,
        'quit': quitcmd.command,
        'r': reset.command,
        'reg': register.command,
        'register': register.command,
        'reset': reset.command,
        'rules': rules.command,
        's': search.command,
        'search': search.command,
        'sh': show.command,
        'show': show.command,
        'u': update.command,
        'unreg': unregister.command,
        'unregister': unregister.command,
        'update': update.command,
        'w': watch.command,
        'watch': watch.command,
    }
    safe_exceptions = set([AIDParseError])

    def __init__(self, config):
        self.state = State()
        self.last_cmd = []

        self.config = config
        self.titles = TitleSearcher(config['anime'].getpath('anidb_cache'))
        dbfile = config['anime'].getpath('database')
        self.conn = self.db = self._connect(dbfile)

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
                    if command(self.state, tokens):
                        break
            except ParseExit:
                continue
            except Exception as e:
                if e not in self.safe_exceptions:
                    logger.exception('Error!')

    def _connect(self, dbfile: 'PathLike') -> apsw.Connection:
        """Connect to SQLite database file."""
        conn = apsw.Connection(os.fspath(dbfile))
        _set_foreign_keys(conn, 1)
        assert _get_foreign_keys(conn) == 1
        return conn

    @mir.cp.NonDataCachedProperty
    def file_picker(self) -> FilePicker:
        """Cached file picker property."""
        return FilePicker(
            Rule(rule.regexp, rule.priority)
            for rule in query.files.get_priority_rules(self.db))


@dataclass
class State:
    ...


def _get_foreign_keys(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys')
    return cur.fetchone()[0]


def _set_foreign_keys(conn, value: int):
    cur = conn.cursor()
    cur.execute(f'PRAGMA foreign_keys={value:d}')
