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

"""Bump command."""

from collections import OrderedDict
from datetime import date
import logging

from animanager import dblib
from animanager import inputlib

_LOGGER = logging.getLogger(__name__)


def _search(dbconfig, name):
    """Search for series that are being watched."""
    results = dblib.select(
        dbconfig,
        table='anime',
        fields=['id', 'name', 'ep_watched', 'ep_total', 'status'],
        where_filter='name LIKE %s AND status = "watching"',
        where_args=('%{}%'.format(name),),
    )
    results = list(results)
    return results


def _search_all(dbconfig, name):
    """Search for all non-complete series."""
    results = dblib.select(
        dbconfig,
        table='anime',
        fields=['id', 'name', 'ep_watched', 'ep_total', 'status'],
        where_filter='name LIKE %s AND status != "complete"',
        where_args=('%{}%'.format(name),),
    )
    results = list(results)
    return results


def ibump(dbconfig, choices):
    "Interactively bump anime episode count."""
    i = inputlib.get_choice(['({}) {}'.format(x[0], x[1]) for x in choices])
    choice = choices[i]
    choice_id = choice[0]
    watched, total, status = choice[2:]

    assert (total == 0) or (watched <= total)
    if watched == total and total != 0:
        print('Maxed')
        return

    # Confirm choice
    print('Currently {}/{}'.format(watched, total))
    if not inputlib.get_yn("Bump?"):
        print('Aborting...')
        return

    # MySQL connector returns a set type because it is retarded.
    # We need to convert it.
    status = dblib.convert_set(status)
    assert isinstance(status, str)

    # Calculate what needs updating.
    update_map = OrderedDict()
    watched += 1
    print('Now {}/{}'.format(watched, total))
    update_map['ep_watched'] = watched

    if status != 'watching':
        assert status in ('on hold', 'dropped', 'plan to watch')
        update_map['status'] = 'watching'
        if status == 'plan to watch':
            update_map['date_started'] = date.today().isoformat()

    dblib.update_one(dbconfig,
                     'anime',
                     update_map.keys(),
                     [choice_id] + list(update_map.values()))


def main(args):
    """Bump command."""
    dbconfig = args.config['db_args']
    if args.all:
        choices = _search_all(dbconfig, args.name)
    else:
        choices = _search(dbconfig, args.name)
    ibump(dbconfig, choices)
