# Copyright (C) 2016-2018  Allen Li
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

"""Date timestamp utilities."""

import datetime


def to_ts(date: datetime.date) -> float:
    """Convert date to timestamp.

    >>> to_ts(datetime.date(2001, 1, 2))
    978393600.0
    """
    return datetime.datetime(
        date.year, date.month, date.day,
        tzinfo=datetime.timezone.utc).timestamp()


def to_date(ts: float) -> datetime.date:
    """Convert timestamp to date.

    >>> to_date(978393600.0)
    datetime.date(2001, 1, 2)
    """
    return datetime.datetime.fromtimestamp(
        ts, tz=datetime.timezone.utc).date()
