# Copyright (C) 2015  Allen Li
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

"""Config loading stuff."""

import configparser
import os
import re


class Config:

    defaultpath = os.path.join(os.environ['HOME'], '.animanager', 'config.ini')

    def __init__(self, path=None):
        if path is None:
            path = self.defaultpath()
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

    def save(self):
        with open(self.path, 'w') as file:
            self.config.write(file)

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def register(self, db, id):
        results = db.select(
            table='anime',
            fields=['name'],
            where_filter='id=?',
            where_args=(id,)
        )
        name = next(results)[0]
        self['series'][str(id)] = ''.join((
            r'.*{}.*?'.format(re.escape(name)),
            r'(?P<ep>[0-9]+)',
        ))

    def unregister(self, id):
        del self['series'][str(id)]
