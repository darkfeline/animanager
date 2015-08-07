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

"""
Automated anime watching and tracking script.
"""

import logging
import os
import subprocess
import re
from operator import itemgetter

from animanager import inputlib

from .bump import bump

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=main)


def _get_series_info(db, config):
    """Get series info.

    Load series id and filename patterns from the config file and match it with
    other necessary info from our database.

    Output format: A list of tuples (id, pattern, name, ep_watched)

    pattern: Compiled regexp pattern

    """
    processed_list = []
    for id, pattern in config['series'].items():
        id = int(id)
        # Get series information from database.
        results = db.select(
            table='anime',
            fields=['name', 'ep_watched'],
            where_filter='id=?',
            where_args=(id,),
        )
        name, ep_watched = list(results)[0]
        pattern = re.compile(pattern)
        processed_list.append((id, pattern, name, ep_watched))
    return processed_list


def _match_series_files(series_info, files):
    """Match series files.

    Use series information to associate with the given list of files.

    Takes input series_info from _get_series_info().

    """
    series_files = [x + (list(),) for x in series_info]
    for filename in files:
        for id, pattern, name, ep_watched, matched_files in series_files:
            match = pattern.match(filename)
            if match:
                # Even if we match a file, we still check the episode number.
                # If it has already been watched, remove the file and don't add
                # it.
                ep_num = int(match.group('ep'))
                if ep_num <= ep_watched:
                    os.remove(filename)
                    msg = 'Removed {} because it has already been watched.'
                    _LOGGER.info(msg.format(filename))
                else:
                    matched_files.append((ep_num, filename))
                break
    return [[id, name, ep_watched, sorted(matched_files, key=itemgetter(0))]
            for id, pattern, name, ep_watched, matched_files in series_files
            if matched_files]


def main(args):

    config = args.config
    db = args.db
    player = config['watch']['player']

    # Load series information.
    series_info = _get_series_info(db, config)

    # Use series information to search current directory for files and
    # match them with a series.
    files = sorted(os.listdir('.'))
    series_files = _match_series_files(series_info, files)

    while True:
        # Choose series to watch.
        msg = "({}) {} (cur. ep. {}, {} eps. avail.)"
        i = inputlib.get_choice(
            [msg.format(id, name, ep_watched, len(matched_files))
             for id, name, ep_watched, matched_files in series_files]
        )

        id, _, ep_watched, files = series_files[i]

        # Check if next episode has the right number.
        if files[0][0] != ep_watched + 1:
            print('Next episode is missing.')
            continue

        # Play the episode.
        subprocess.call([player, files[0][1]])

        if inputlib.get_yn('Bump?'):
            bump(db, id)

        if inputlib.get_yn('Delete?'):
            os.unlink(files[0][1])

        # Remove the episode from our list.
        del files[0]
        # Also remove the series if there are no more episodes.
        if not files:
            del series_files[i]
