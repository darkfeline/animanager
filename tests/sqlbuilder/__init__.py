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

    def _test_builder(self, builder, expected):
        query = builder.build()
        self.assertEqual(query, expected)

    def test_select(self):
        builder = sqlbuilder.Select('table')
        builder.add_column('foo')
        builder.add_column('bar')
        expected = 'SELECT "foo" , "bar" FROM "table"'
        self._test_builder(builder, expected)

    def test_select_where(self):
        self.skipTest('not done yet')
        builder = sqlbuilder.Select('table')
        builder.add_column('foo')
        builder.add_column('bar')
        builder.where(Expr())

        expected = 'SELECT "foo" , "bar" FROM "table"'
        self._test_builder(builder, expected)

    def test_insert(self):
        builder = sqlbuilder.Insert('table')
        builder.add_column('foo')
        builder.add_column('bar')
        expected = 'INSERT INTO "table" ( "foo" , "bar" ) VALUES ( ? , ? )'
        self._test_builder(builder, expected)

    def test_create_table(self):
        builder = sqlbuilder.CreateTable('table')
        builder.add_column('foo')
        builder.add_column('bar')
        expected = 'CREATE TABLE "table" ( "foo" , "bar" )'
        self._test_builder(builder, expected)

    def test_create_table_with_types(self):
        builder = sqlbuilder.CreateTable('table')
        builder.add_column('foo', type='INTEGER')
        builder.add_column('bar', type='TEXT')
        expected = 'CREATE TABLE "table" ( "foo" INTEGER , "bar" TEXT )'
        self._test_builder(builder, expected)

    def test_create_table_with_pk(self):
        builder = sqlbuilder.CreateTable('table')
        builder.add_column('foo', pk=True)
        builder.add_column('bar')
        expected = ' '.join(('CREATE TABLE "table" ( "foo" , "bar" ,',
                             'PRIMARY KEY ( "foo" ) )'))
        self._test_builder(builder, expected)
