# Copyright (C) 2015-2017  Allen Li
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

import unittest

from apsw import Connection

from animanager.sqlite import utils


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.db = Connection(':memory:')
        cur = self.db.cursor()
        cur.execute("""
        CREATE TABLE mytable (
            id INTEGER PRIMARY KEY,
            firstname TEXT,
            lastname TEXT)""")
        cur.execute("""
        INSERT INTO mytable (id, firstname, lastname)
        VALUES
        (1, 'Mir', 'Jakuri')
        """)

    def test_upsert_insert(self):
        utils.upsert(self.db, 'mytable', ['id'], {
            'id': 2,
            'firstname': 'Ion',
            'lastname': 'Preciel',
        })
        cur = self.db.cursor()
        cur.execute('SELECT * FROM mytable')
        self.assertEqual((1, 'Mir', 'Jakuri'), cur.fetchone())
        self.assertEqual((2, 'Ion', 'Preciel'), cur.fetchone())

    def test_upsert_update(self):
        utils.upsert(self.db, 'mytable', ['id'], {
            'id': 1,
            'lastname': 'Teiwaz',
        })
        cur = self.db.cursor()
        cur.execute('SELECT * FROM mytable')
        self.assertEqual((1, 'Mir', 'Teiwaz'), cur.fetchone())


class MultipleKeyTestCase(unittest.TestCase):

    def setUp(self):
        self.db = Connection(':memory:')
        cur = self.db.cursor()
        cur.execute("""
        CREATE TABLE mytable (
            firstname TEXT,
            lastname TEXT,
            age INTEGER
        )""")
        cur.execute("""
        INSERT INTO mytable (firstname, lastname, age)
        VALUES
        ('Mir', 'Jakuri', 10)
        """)

    def test_upsert_multiple_key_insert(self):
        utils.upsert(self.db, 'mytable', ['firstname', 'lastname'], {
            'firstname': 'Mir',
            'lastname': 'Teiwaz',
            'age': 350,
        })
        cur = self.db.cursor()
        cur.execute('SELECT * FROM mytable')
        self.assertEqual(('Mir', 'Jakuri', 10), cur.fetchone())
        self.assertEqual(('Mir', 'Teiwaz', 350), cur.fetchone())

    def test_upsert_multiple_key_update(self):
        utils.upsert(self.db, 'mytable', ['firstname', 'lastname'], {
            'firstname': 'Mir',
            'lastname': 'Jakuri',
            'age': 350,
        })
        cur = self.db.cursor()
        cur.execute('SELECT * FROM mytable')
        self.assertEqual(('Mir', 'Jakuri', 350), cur.fetchone())
