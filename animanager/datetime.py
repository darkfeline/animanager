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

from datetime import datetime
from datetime import timedelta
from datetime import timezone

EPOCH = datetime.fromtimestamp(0, timezone.utc).date()


def daystamp(date):
    """Return days relative to epoch.

    >>> from datetime import date
    >>> daystamp(date(2001, 1, 2))
    11324

    """
    return (date - EPOCH).days


def fromdaystamp(ds):
    """Convert daystamp into date.

    >>> fromdaystamp(11324)
    datetime.date(2001, 1, 2)

    """
    return EPOCH + timedelta(days=ds)


def parse_date(string):
    """Parse an ISO format date (YYYY-mm-dd).

    >>> parse_date('1990-01-02')
    datetime.date(1990, 1, 2)

    """
    return datetime.strptime(string, '%Y-%m-%d').date()
