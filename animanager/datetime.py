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

import datetime


def unix_timestamp(dt):
    """Turn datetime-like object into UNIX timestamp.

    >>> unix_timestamp(datetime.datetime(2001, 1, 2, 10, 11, 12))
    978459072.0

    >>> unix_timestamp(datetime.date(2001, 1, 2))
    978422400.0

    """
    if isinstance(dt, datetime.date):
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    if isinstance(dt, datetime.datetime):
        return dt.timestamp()
    raise TypeError('dt is not datetime-like')


def parse_date(string):
    """Parse an ISO format date (YYYY-mm-dd).

    >>> parse_date('1990-01-02')
    datetime.date(1990, 1, 2)

    """
    return datetime.datetime.strptime(string, '%Y-%m-%d').date()
