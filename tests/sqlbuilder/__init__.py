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

import unittest

from animanager import sqlbuilder

from . import tokens


def load_tests(loader, tests, pattern):
    tests.addTest(loader.loadTestsFromModule(tokens))
    return tests


class SQLBuilderTestCase(unittest.TestCase):

    def test_select(self):
        query = sqlbuilder.Select('table')
        query.add_column('foo')
        query.add_column('bar')
        query = query.build()
        expected = 'SELECT "foo" , "bar" FROM "table"'
        self.assertEqual(query, expected)

    def test_insert(self):
        query = sqlbuilder.Insert('table')
        query.add_column('foo')
        query.add_column('bar')
        query = query.build()
        expected = 'INSERT INTO "table" ( "foo" , "bar" ) VALUES ( ? , ? )'
        self.assertEqual(query, expected)

    def test_create_table(self):
        query = sqlbuilder.CreateTable('table')
        query.add_column('foo')
        query.add_column('bar')
        query = query.build()
        expected = 'CREATE TABLE "table" ( "foo" , "bar" )'
        self.assertEqual(query, expected)

    def test_create_table_with_types(self):
        query = sqlbuilder.CreateTable('table')
        query.add_column('foo', type='INTEGER')
        query.add_column('bar', type='TEXT')
        query = query.build()
        expected = 'CREATE TABLE "table" ( "foo" INTEGER , "bar" TEXT )'
        self.assertEqual(query, expected)

    def test_create_table_with_pk(self):
        query = sqlbuilder.CreateTable('table')
        query.add_column('foo', pk=True)
        query.add_column('bar')
        query = query.build()
        expected = ' '.join(('CREATE TABLE "table" ( "foo" , "bar" ,',
                             'PRIMARY KEY ( "foo" ) )'))
        self.assertEqual(query, expected)
