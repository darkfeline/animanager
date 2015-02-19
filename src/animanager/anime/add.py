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

"""Implements add command."""

from collections import OrderedDict
from datetime import date
import logging

from animanager import dblib
from animanager import inputlib
from animanager import mal

_LOGGER = logging.getLogger(__name__)
_STATUSES = ('plan to watch', 'watching', 'complete')


def main(args):

    """Add command."""

    config = args.config
    name = args.name

    # Get choices from MAL API
    mal.setup(config)
    results = mal.anime_search(name)
    i = inputlib.get_choice(['{} {}'.format(x.id, x.title) for x in results])

    # Set data fields
    chosen = results[i]
    fields = OrderedDict((
        ('animedb_id', chosen.id),
        ('name', chosen.title),
        ('ep_total', chosen.episodes),
        ('type', chosen.type),
    ))

    # Choose status to set
    i = inputlib.get_choice(_STATUSES, 0)
    fields['status'] = _STATUSES[i]
    if fields['status'] == 'watching':
        confirm = input('Set start date to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            fields['date_started'] = date.today().isoformat()
    elif fields['status'] == 'complete':
        fields['ep_watched'] = fields['ep_total']
        confirm = input('Set dates to today? [Y/n]')
        if confirm.lower() not in ('n', 'no'):
            today = date.today().isoformat()
            fields['date_started'] = today
            fields['date_finished'] = today

    dblib.insert(config['db_args'], 'anime', fields)
