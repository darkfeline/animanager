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


class AIDParseError(Exception):
    pass


class InvalidSyntaxError(ValueError, AIDParseError):

    def __init__(self, text):
        self.text = text
        super().__init__('Invalid syntax: {}'.format(text))


class InvalidResultKeyError(KeyError, AIDParseError):

    def __init__(self, key):
        self.key = key
        super().__init__('Invalid result key {}'.format(key))


class InvalidResultNumberError(IndexError, AIDParseError):

    def __init__(self, key, number):
        self.key = key
        self.number = number
        super().__init__('Invalid number {} for key {}'.format(
            number, key))
