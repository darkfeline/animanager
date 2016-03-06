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
from animanager.sqlbuilder import errors
from animanager.sqlbuilder.expr import *


class SQLBuilderTestCase(unittest.TestCase):

    # These are test names, so they can be longer than normal.
    # pylint: disable=invalid-name

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
        builder = sqlbuilder.Select('table')
        builder.add_column('foo')
        builder.add_column('bar')
        builder.where(BinaryOp('=', Identifier('foo'), literal('spam')))
        expected = 'SELECT "foo" , "bar" FROM "table" WHERE "foo" = \'spam\''
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
        builder.add_column('foo', type_name='INTEGER')
        builder.add_column('bar', type_name='TEXT')
        expected = 'CREATE TABLE "table" ( "foo" "INTEGER" , "bar" "TEXT" )'
        self._test_builder(builder, expected)

    def test_create_table_with_primary_key(self):
        builder = sqlbuilder.CreateTable('table')
        builder.add_column('foo', primary_key=True)
        builder.add_column('bar')
        expected = ' '.join(('CREATE TABLE "table" ( "foo" , "bar" ,',
                             'PRIMARY KEY ( "foo" ) )'))
        self._test_builder(builder, expected)

    def test_column(self):
        builder = sqlbuilder.CreateTable.Column('foo')
        expected = '"foo"'
        self._test_builder(builder, expected)

    def test_column_with_type(self):
        builder = sqlbuilder.CreateTable.Column('foo', type_name='INTEGER')
        expected = '"foo" "INTEGER"'
        self._test_builder(builder, expected)

    def test_column_with_bad_type(self):
        self.assertRaises(
            TypeError,
            sqlbuilder.CreateTable.Column, 'foo', type_name=9)

    def test_primary_key(self):
        builder = sqlbuilder.CreateTable.PrimaryKey()
        builder.add_column('foo')
        expected = 'PRIMARY KEY ( "foo" )'
        self._test_builder(builder, expected)

    def test_primary_key_multiple(self):
        builder = sqlbuilder.CreateTable.PrimaryKey()
        builder.add_column('foo')
        builder.add_column('bar')
        expected = 'PRIMARY KEY ( "foo" , "bar" )'
        self._test_builder(builder, expected)

    def test_primary_key_empty(self):
        builder = sqlbuilder.CreateTable.PrimaryKey()
        self.assertFalse(builder)

    def test_primary_key_nonempty(self):
        builder = sqlbuilder.CreateTable.PrimaryKey()
        builder.add_column('foo')
        self.assertTrue(builder)

    def test_primary_invalid_build(self):
        builder = sqlbuilder.CreateTable.PrimaryKey()
        self.assertRaises(errors.IncompleteQueryError, builder.build)
