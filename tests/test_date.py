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
from datetime import datetime, timezone

import hypothesis
from hypothesis import strategies

import animanager.date

MIN_DATETIME = datetime(1970, 1, 1, tzinfo=timezone.utc)
MAX_DATETIME = datetime(2038, 12, 31, tzinfo=timezone.utc)
MIN_TIMESTAMP = MIN_DATETIME.timestamp()
MAX_TIMESTAMP = MAX_DATETIME.timestamp()


@strategies.composite
def datetimes(draw):
    return datetime.fromtimestamp(
        draw(strategies.floats(
            MIN_TIMESTAMP,
            MAX_TIMESTAMP,
        )),
        tz=timezone.utc,
    )


@strategies.composite
def dates(draw):
    return draw(datetimes()).date()


class DateTimeTestCase(unittest.TestCase):

    @hypothesis.given(dates())
    def test_timestamp(self, date):
        ts = animanager.date.timestamp(date)
        new_date = animanager.date.fromtimestamp(ts)
        self.assertEqual(date, new_date)
