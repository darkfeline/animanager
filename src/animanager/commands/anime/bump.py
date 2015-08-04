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

from datetime import date
import logging

from animanager import inputlib

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'bump',
        description='Bump the episode count of a watched series.',
        help='Bump the episode count of a watched series.',
    )
    parser.add_argument('name', help='String to search for.')
    parser.add_argument('--all', action='store_true',
                        help='Search all non-complete series.')
    parser.set_defaults(func=main)


def _search(db, name, all=False):
    """Search for series."""
    if all:
        where_filter = 'name LIKE ? AND status!="complete"'
    else:
        where_filter = 'name LIKE ? AND status="watching"'
    results = db.select(
        table='anime',
        fields=['id', 'name', 'ep_watched', 'ep_total', 'status'],
        where_filter=where_filter,
        where_args=('%{}%'.format(name),),
    )
    results = list(results)
    return results


def ibump(db, choices):
    "Interactively bump anime episode count."""

    # There's a lot of stuff to do here.
    # First, we prompt the user to choose a series to bump.
    i = inputlib.get_choice(['({}) {}'.format(x[0], x[1]) for x in choices])
    choice = choices[i]
    choice_id = choice[0]
    watched, total, status = choice[2:]

    if watched == total and total != 0:
        print('Maxed')
        return

    # Confirm choice.
    print('Currently {}/{}'.format(watched, total))
    if not inputlib.get_yn("Bump?"):
        print('Aborting...')
        return

    # Calculate what needs updating, putting it into a dictionary that we will
    # update at the end all at once.
    update_map = dict()
    # First we update the episode count.
    watched += 1
    print('Now {}/{}'.format(watched, total))
    update_map['ep_watched'] = watched

    # If the status wasn't watching, we set it so.
    # Additionally if it was plan to watch, we set the starting date.
    if status != 'watching':
        update_map['status'] = 'watching'
        if status == 'plan to watch':
            update_map['date_started'] = date.today().isoformat()

    # Finally, if the series is now complete, we set the status and finish date
    # accordingly.
    if watched == total and total != 0:
        update_map['status'] = 'complete'
        update_map['date_finished'] = date.today().isoformat()

    # Now we update all of the changes we have gathered.
    db.update_one(
        'anime',
        update_map.keys(),
        [choice_id] + list(update_map.values()))


def main(args):
    """Bump command."""
    choices = _search(args.db, args.name, args.all)
    ibump(args.db, choices)
