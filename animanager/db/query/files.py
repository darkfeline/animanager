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

"""File picking related queries."""

from collections import namedtuple
from typing import Iterable, Optional

from animanager.files import AnimeFiles
from animanager.sqlite import upsert

from .status import cache_status, get_complete

PriorityRule = namedtuple(
    'PriorityRule',
    ['id', 'regexp', 'priority'])


def get_priority_rules(db) -> Iterable[PriorityRule]:
    """Get file priority rules."""
    cur = db.cursor()
    cur.execute('SELECT id, regexp, priority FROM file_priority')
    for row in cur:
        yield PriorityRule(*row)


def add_priority_rule(
        db, regexp: str, priority: Optional[int] = None,
) -> int:
    """Add a file priority rule."""
    with db:
        cur = db.cursor()
        if priority is None:
            cur.execute('SELECT MAX(priority) FROM file_priority')
            highest_priority = cur.fetchone()[0]
            if highest_priority is None:
                priority = 1
            else:
                priority = highest_priority + 1
        cur.execute("""
            INSERT INTO file_priority (regexp, priority)
            VALUES (?, ?)""", (regexp, priority))
        row_id = db.last_insert_rowid()
    return row_id


def delete_priority_rule(db, rule_id: int) -> None:
    """Delete a file priority rule."""
    with db:
        cur = db.cursor()
        cur.execute('DELETE FROM file_priority WHERE id=?', (rule_id,))


def cache_files(db, aid: int, anime_files: AnimeFiles) -> None:
    """Cache files for anime."""
    with db:
        cache_status(db, aid)
        db.cursor().execute(
            """UPDATE cache_anime
            SET anime_files=?
            WHERE aid=?""",
            (anime_files.to_json(), aid))


def get_files(conn, aid: int) -> AnimeFiles:
    """Get cached files for anime."""
    with conn:
        cur = conn.cursor().execute(
            'SELECT anime_files FROM cache_anime WHERE aid=?',
            (aid,))
        row = cur.fetchone()
        if row is None:
            raise ValueError('No cached files')
        return AnimeFiles.from_json(row[0])


def set_regexp(db, aid, regexp):
    """Set watching regexp for anime."""
    upsert(db, 'watching', ['aid'], {'aid': aid, 'regexp': regexp})


def delete_regexp(db, aid):
    """Delete watching regexp for anime."""
    db.cursor().execute(
        """DELETE FROM watching WHERE aid=?""",
        (aid,))


def delete_regexp_complete(db):
    """Delete watching regexp for complete anime."""
    db.cursor().executemany(
        """DELETE FROM watching WHERE aid=?""",
        ((aid,) for aid in get_complete(db)))
