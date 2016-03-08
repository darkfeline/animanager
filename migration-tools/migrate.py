"""Migrate data to new Animanager format."""

import logging
import os
import sqlite3
import sys

import anidb
from paths import ANIDB, NEW, OLD


def cachepath(aid):
    """Return path to corresponding AniDB data file."""
    return os.path.join(ANIDB, '{}.xml'.format(aid))


def lookup(aid):
    """Return lookup tree for given AID."""
    return anidb.LookupTree.parse(cachepath(aid))


def migrate(cnx):
    cnx.execute("""
    CREATE TABLE anime (
        aid INTEGER,
        title TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        episodes INTEGER,
        startdate DATE,
        enddate DATE,
        PRIMARY KEY (aid)
    )""")
    cnx.execute("""
    CREATE TABLE "episode" (
        id INTEGER,
        aid INTEGER NOT NULL,
        type INTEGER NOT NULL,
        number INTEGER NOT NULL,
        title TEXT NOT NULL,
        length INTEGER NOT NULL,
        user_watched INTEGER NOT NULL CHECK (user_watched IN (0, 1)),
        PRIMARY KEY (id),
        UNIQUE (aid, type, number),
        FOREIGN KEY (aid) REFERENCES anime (aid)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (type) REFERENCES episode_type (id)
            ON DELETE RESTRICT ON UPDATE CASCADE
    )""")
    cnx.execute("""
    CREATE TABLE episode_type (
        id INTEGER,
        name TEXT NOT NULL UNIQUE,
        prefix TEXT NOT NULL UNIQUE,
        PRIMARY KEY(id)
    )""")
    cnx.execute("""
    INSERT INTO episode_type
    (id, name, prefix)
    VALUES
    (1, 'regular', ''),
    (2, 'special', 'S'),
    (3, 'credit', 'C'),
    (4, 'trailer', 'T'),
    (5, 'parody', 'P'),
    (6, 'other', 'O')
    """)
    cnx.execute("""
    CREATE TABLE watching (
        aid INTEGER,
        regexp TEXT NOT NULL,
        PRIMARY KEY (aid),
        FOREIGN KEY (aid) REFERENCES anime (aid)
            ON DELETE CASCADE ON UPDATE CASCADE
    )""")


def main():
    logging.basicConfig(level='DEBUG',
                        format='%(asctime)s:%(levelname)s:%(message)s')

    conn_old = sqlite3.connect(OLD)
    if os.path.exists(NEW):
        print('Please remove {} first'.format(NEW))
        sys.exit(1)
    conn_new = sqlite3.connect(NEW)
    migrate(conn_new)
    idmap = dict()

    def add_id(id, aid):
        idmap[id] = aid

    ###########################################################################
    # Add all anime with AIDs.
    cur = conn_old.execute(' '.join((
        'SELECT id, anidb_id',
        'FROM anime WHERE anidb_id IS NOT NULL')))

    for row in cur:
        id, aid = row
        tree = lookup(aid)
        add_id(id, aid)

        conn_new.execute(
            ' '.join((
                'INSERT INTO anime',
                '(aid, title, type, episodes, startdate, enddate)',
                'VALUES (?, ?, ?, ?, ?, ?)',
            )),
            (aid, tree.title, tree.type, tree.episodecount,
             tree.startdate, tree.enddate)
        )

    ###########################################################################
    # Add episodes for completed items.
    cur = conn_old.execute(' '.join((
        'SELECT id, anidb_id',
        'FROM anime WHERE status="complete" AND anidb_id IS NOT NULL')))

    for row in cur:
        id, aid = row
        tree = lookup(aid)
        id = idmap[id]

        # Add episodes.
        conn_new.executemany(
            ' '.join((
                'INSERT INTO episode',
                '(aid, type, number, title, length,',
                'user_watched)',
                'VALUES (?, ?, ?, ?, ?, ?)',
            )),
            ((id, ep.type, ep.number, ep.title, ep.length,
              1 if ep.type == 1 else 0)  # Mark regular episodes as watched.
             for ep in tree.episodes)
        )

    ###########################################################################
    # Add episodes for plan to watch items.
    cur = conn_old.execute(' '.join((
        'SELECT id, anidb_id',
        'FROM anime WHERE status="plan to watch" AND anidb_id IS NOT NULL')))

    for row in cur:
        id, aid = row
        tree = lookup(aid)
        id = idmap[id]

        # Add episodes.
        conn_new.executemany(
            ' '.join((
                'INSERT INTO episode',
                '(aid, type, number, title, length,',
                'user_watched)',
                'VALUES (?, ?, ?, ?, ?, ?)',
            )),
            ((id, ep.type, ep.number, ep.title, ep.length, 0)
             for ep in tree.episodes)
        )

    ###########################################################################
    # Add episodes for watching, on hold, and dropped items.
    cur = conn_old.execute(' '.join((
        'SELECT id, anidb_id, ep_watched',
        'FROM anime WHERE status IN ("watching", "on hold", "dropped")',
        'AND anidb_id IS NOT NULL')))

    for row in cur:
        id, aid, watched = row
        tree = lookup(aid)
        id = idmap[id]

        # Add episodes.
        conn_new.executemany(
            ' '.join((
                'INSERT INTO episode',
                '(aid, type, number, title, length,',
                'user_watched)',
                'VALUES (?, ?, ?, ?, ?, ?)',
            )),
            ((id, ep.type, ep.number, ep.title, ep.length,
              1 if ep.type == 1 and ep.number <= watched else 0)
             for ep in tree.episodes)
        )

    conn_new.commit()


if __name__ == '__main__':
    main()
