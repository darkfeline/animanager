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


def ibump(dbconfig, name):
    "Interactively bump anime."""
    results = dblib.select(dbconfig,
                           'anime',
                           ['id', 'name', 'ep_watched', 'ep_total', 'status'],
                           'name LIKE %s AND status != "complete"',
                           ('%{}%'.format(name),))
    results = list(results)
    i = inputlib.get_choice(
        ['{} {}'.format(x[0], x[1]) for x in results])
    choice = results[i]
    choice_id = choice[0]
    watched, total, status = choice[2:]

    # Confirm choice
    if watched >= total and total != 0:
        print('Maxed')
        return
    print('Bumping {}/{}'.format(watched, total))
    confirm = input("Okay? [Y/n]")
    if confirm.lower() in ('n', 'no'):
        print('Quitting')
        return

    # MySQL connector returns a set type because it is retarded.
    # We need to convert it.
    status = list(status)
    assert len(status) == 1
    status = status[0]
    assert isinstance(status, str)

    # Calculate what needs updating
    update_map = OrderedDict()
    watched += 1
    print('Now {}/{}'.format(watched, total))
    update_map['ep_watched'] = watched

    if status in ('on hold', 'dropped', 'plan to watch'):
        print('Setting status to "watching"')
        update_map['status'] = 'watching'
    if status == 'plan to watch':
        print('Setting start date')
        update_map['date_started'] = date.today().isoformat()
    if watched == total and total != 0:
        print('Setting status to "complete"')
        update_map['status'] = 'complete'

    dblib.update_one(dbconfig,
                     'anime',
                     update_map.keys(),
                     [choice_id] + list(update_map.values()))


def main(args):
    """Bump command."""
    name = args.name
    dbconfig = args.config['db_args']
    ibump(dbconfig, name)
