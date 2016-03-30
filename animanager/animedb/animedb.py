# Copyright (C) 2015-2016  Allen Li
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
from typing import Dict

from animanager import db
from animanager.cache import cached_property

from . import migrations
from .cache import AnimeCacheMixin
from .collections import EpisodeType
from .files import FilesMixin
from .select import SelectMixin
from .status import StatusMixin
from .update import UpdateMixin

logger = logging.getLogger(__name__)


class AnimeDB(
        SelectMixin,
        UpdateMixin,
        FilesMixin,
        StatusMixin,
        AnimeCacheMixin,
        db.UserVersionMixin,
        db.MigrationMixin,
        db.ForeignKeyMixin,
        db.SQLiteDB,
): # pylint: disable=too-many-ancestors

    """Our anime database."""

    def __init__(self, database):
        self.database = database
        super().__init__(database)

    @property
    def version(self):
        return self.migration_manager.current_version

    @property
    def migration_manager(self):
        return migrations.manager

    def migrate(self):
        if self.needs_migration():
            logger.info('Migration needed, backing up database')
            shutil.copyfile(self.database, self.database + '~')
            logger.info('Migrating database')
            super().migrate()

    def purge_cache(self):
        super().purge_cache()
        del self.episode_types
        del self.episode_types_by_id
        del self.priority_rules

    @cached_property
    def episode_types(self) -> Dict[int, EpisodeType]:
        """Episode types.

        Returns a dictionary mapping episode type name strings to EpisodeType
        instances.

        """
        ep_types = dict()
        cur = self.cnx.cursor()
        cur.execute('SELECT id, name, prefix FROM episode_type')
        for type_id, name, prefix in cur:
            ep_types[name] = EpisodeType(type_id, prefix)
        return ep_types

    @cached_property
    def episode_types_by_id(self) -> Dict[str, EpisodeType]:
        """Episode types by id.

        Returns a dictionary mapping episode type ids to EpisodeType
        instances.

        """
        ep_types = dict()
        cur = self.cnx.cursor()
        cur.execute('SELECT id, prefix FROM episode_type')
        for type_id, prefix in cur:
            ep_types[type_id] = EpisodeType(type_id, prefix)
        return ep_types

    def get_epno(self, episode):
        """Return epno for Episode instance.

        epno is a string formatted with the episode number and type,
        e.g., S1, T2.

        """
        return '{}{}'.format(self.episode_types_by_id[episode.type].prefix,
                             episode.number)
