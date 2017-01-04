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

import logging
import shutil
from textwrap import dedent

import animanager.descriptors
from animanager import __version__ as VERSION
from animanager.anidb.titles import TitleSearcher
from animanager.cmd import Cmd
from animanager.cmd.results import AIDParseError, AIDResults, AIDResultsManager
from animanager.db import cachetable, migrations, query
from animanager.files import FilePicker, Rule
from animanager.sqlite import SQLiteDB

# pylint: disable=import-self
from . import (
    add, addrule, asearch, bump, deleterule, gpl, helpcmd, purgecache,
    quitcmd, register, reset, rules, search, show, unregister, update, watch,
)

logger = logging.getLogger(__name__)


class AnimeCmd(Cmd):

    """Animanager anime CLI."""

    intro = dedent('''\
    Animanager {}
    Copyright (C) 2015-2016  Allen Li

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
        self.db = SQLiteDB(dbfile)

        manager = migrations.manager
        if manager.should_migrate(self.db):
            logger.info('Migration needed, backing up database')
            shutil.copyfile(dbfile, dbfile + '~')
            logger.info('Migrating database')
            manager.migrate(self.db)

        self.cache_manager = cachetable.make_manager(self.db)
        self.cache_manager.setup()

        self.results = AIDResultsManager({
            'db': AIDResults([
                'Title', 'Type', 'Episodes', 'Complete', 'Available',
            ]),
            'anidb': AIDResults(['Title']),
        })

    @animanager.descriptors.CachedProperty
    def file_picker(self) -> FilePicker:
        """Cached file picker property."""
        return FilePicker(
            Rule(rule.regexp, rule.priority)
            for rule in query.files.get_priority_rules(self.db))
