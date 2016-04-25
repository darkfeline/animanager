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

# pylint: disable=import-self

import logging
import shutil
from textwrap import dedent

from animanager import __version__ as VERSION
from animanager.anidb.titles import TitleSearcher
from animanager.cmd import Cmd
from animanager.cmd.results import AIDParseError, AIDResults, AIDResultsManager
from animanager.db import cachetable, migrations
from animanager.db.query.files import PriorityRules
from animanager.files import FilePicker, Rule
from animanager.sqlite import SQLiteDB
from animanager.utils import cached_property

from . import gpl, purgecache, quitcmd

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
        'gpl': gpl.command,
        'purgecache': purgecache.command,
        'q': quitcmd.command,
        'quit': quitcmd.command,
    }
    safe_exceptions = set([AIDParseError])

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config
        self.titles = TitleSearcher(config.anime.anidb_cache)
        dbfile = config.anime.database
        self.db = SQLiteDB(dbfile)

        manager = migrations.manager
        if manager.needs_migration(self.db):
            logger.info('Migration needed, backing up database')
            shutil.copyfile(dbfile, dbfile + '~')
            logger.info('Migrating database')
            manager.migrate(self.db)
        manager.check_version(self.db)

        self.cache_manager = cachetable.make_manager(self.db)
        self.cache_manager.setup()

        self.results = AIDResultsManager({
            'db': AIDResults([
                'Title', 'Type', 'Episodes', 'Complete', 'Available',
            ]),
            'anidb': AIDResults(['Title']),
        })

    @cached_property
    def file_picker(self) -> FilePicker:
        """Cached file picker property."""
        return FilePicker(
            Rule(rule.regexp, rule.priority)
            for rule in PriorityRules.get(self.db))
