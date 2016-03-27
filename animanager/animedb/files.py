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

from typing import List, Optional

from animanager.cache import cached_property
from animanager.files import AnimeFiles
from animanager.files.abc import BaseAnimeFiles

from .collections import PriorityRule


class FilesMixin:

    """File-related rule methods for AnimeDB."""

    def add_priority_rule(
            self, regexp: str, priority: Optional[int] = None,
    ) -> int:
        """Add a file priority rule."""
        with self.cnx:
            cur = self.cnx.cursor()
            if priority is None:
                cur.execute('SELECT MAX(priority) FROM file_priority')
                row = cur.fetchone()  # type: Optional[Tuple[Optional[int]]]
                if cur is None:
                    priority = 1
                else:
                    highest_priority = row[0]
                    if highest_priority is None:
                        priority = 1
                    else:
                        priority = highest_priority + 1
            cur.execute(
                """INSERT INTO file_priority (regexp, priority)
                    VALUES (?, ?)""", (regexp, priority))
            row_id = cur.execute('SELECT last_insert_rowid()').fetchone()[0]
            del self.priority_rules
        return row_id

    @cached_property
    def priority_rules(self) -> List[PriorityRule]:
        """List file priority rules."""
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute('SELECT id, regexp, priority FROM file_priority')
            return [
                PriorityRule(rule_id, regexp, priority)
                for rule_id, regexp, priority in cur]

    def delete_priority_rule(self, rule_id: int) -> None:
        """Delete a file priority rule."""
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute('DELETE FROM file_priority WHERE id=?', (rule_id,))
            del self.priority_rules

    def cache_files(self, aid: int, anime_files: BaseAnimeFiles) -> None:
        with self.cnx:
            self.cache_status(aid)
            self.cnx.cursor().execute(
                """UPDATE cache_anime
                SET anime_files=?
                WHERE aid=?""",
                (anime_files.to_json(), aid))

    def get_files(self, aid: int) -> BaseAnimeFiles:
        with self.cnx:
            cur = self.cnx.cursor().execute(
                'SELECT anime_files FROM cache_anime WHERE aid=?',
                (aid,))
            row = cur.fetchone()
            if row is None:
                raise ValueError('No cached files')
            return AnimeFiles.from_json(row[0])

    def set_regexp(self, aid, regexp):
        """Set watching regexp for anime."""
        with self.cnx:
            cur = self.cnx.cursor()
            cur.execute(
                'UPDATE watching SET regexp=? WHERE aid=?',
                (regexp, aid),
            )
            if self.cnx.changes() == 0:
                cur.execute(
                    """INSERT INTO watching (aid, regexp)
                    VALUES (?, ?)""", (aid, regexp))

    def delete_regexp(self, aid):
        """Delete watching regexp for anime."""
        self.cnx.cursor().execute(
            """DELETE FROM watching WHERE aid=?""",
            (aid,))

    def delete_regexp_complete(self):
        """Delete watching regexp for complete anime."""
        with self.cnx:
            complete = self.get_complete()
            self.cnx.cursor().execute(
                """DELETE FROM watching WHERE aid IN ?""",
                (tuple(complete),))
