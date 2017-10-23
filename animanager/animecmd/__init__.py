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
from os import fspath
import shutil
import sqlite3
from textwrap import dedent

import apsw
import sqlalchemy

import mir.cp

from animanager import __version__ as VERSION
from animanager.anidb.titles import TitleSearcher
from animanager.cmd import Cmd
from animanager.cmd.results import AIDParseError, AIDResults, AIDResultsManager
from animanager.db import cachetable, migrations, query
from animanager.files import FilePicker, Rule

from . import (
    add, addrule, asearch, bump, deleterule, gpl, helpcmd, purgecache,
    quitcmd, register, reset, rules, search, show, unregister, update, watch,
)

logger = logging.getLogger(__name__)


class AnimeCmd(Cmd):

    """Animanager anime CLI."""

    intro = dedent('''\
    Animanager {}
    Copyright (C) 2015-2017  Allen Li

    This program comes with ABSOLUTELY NO WARRANTY; for details type "gpl w".
    This is free software, and you are welcome to redistribute it
    under certain conditions; type "gpl c" for details.''').format(VERSION)
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

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config
        self.titles = TitleSearcher(config.anime.anidb_cache)
        dbfile = config.anime.database
        self.conn = self.db = self._connect(dbfile)
        self.engine = self._connect_engine(dbfile)

        self._migrate(dbfile)

        self.cache_manager = cachetable.make_manager(self.db)
        self.cache_manager.setup()

        self.results = AIDResultsManager({
            'db': AIDResults([
                'Title', 'Type', 'Episodes', 'Complete', 'Available',
            ]),
            'anidb': AIDResults(['Title']),
        })

    def _connect(self, dbfile: 'PathLike') -> apsw.Connection:
        """Connect to SQLite database file."""
        conn = apsw.Connection(os.fspath(dbfile))
        set_foreign_keys(conn, 1)
        assert get_foreign_keys(conn) == 1
        return conn

    def _connect_engine(self, dbfile: 'PathLike') -> sqlalchemy.engine.Engine:
        """Connect to SQLite database file."""
        engine = sqlalchemy.create_engine('sqlite:///' + os.fspath(dbfile))
        return engine

    def _migrate(self, dbfile: 'PathLike'):
        """Do any necessary database migrations."""
        conn = sqlite3.connect(fspath(dbfile))
        manager = migrations.manager
        if manager.should_migrate(conn):
            logger.info('Migration needed, backing up database')
            shutil.copyfile(dbfile, fspath(dbfile) + '~')
            logger.info('Migrating database')
            manager.migrate(conn)
        conn.close()

    @mir.cp.NonDataCachedProperty
    def file_picker(self) -> FilePicker:
        """Cached file picker property."""
        return FilePicker(
            Rule(rule.regexp, rule.priority)
            for rule in query.files.get_priority_rules(self.db))


def get_foreign_keys(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys')
    return cur.fetchone()[0]


def set_foreign_keys(conn, value: int):
    cur = conn.cursor()
    cur.execute(f'PRAGMA foreign_keys={value:d}')
