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

from animanager import inputlib
from animanager import dblib

from .bump import ibump

_LOGGER = logging.getLogger(__name__)


def play(args, filename):
    """Play video."""
    subprocess.call(args + [filename])


def _fetch_series_info(config):
    """Fetch series info.

    Load series id and filename patterns from the config file and match it with
    other necessary info from our database.

    """
    dbconfig = config['db_args']
    series = config['watch']['series']
    # Get the series in our configured list.
    processed_list = []
    for id, pattern in series.items():
        id = int(id)
        # Get series information from database.
        results = dblib.select(
            dbconfig,
            table='anime',
            fields=['name', 'ep_watched'],
            where_filter='id = %s',
            where_args=(id,),
        )
        name, ep_watched = list(results)[0]
        pattern = re.compile(pattern)
        processed_list.append((id, pattern, name, ep_watched))
    return processed_list


# XXX Move this
def filter_series(config):
    """Remove completed series from config file."""
    dbconfig = config['db_args']
    series = config['watch']['series']
    # Get the series in our configured list.
    to_delete = []
    for id, pattern in series.items():
        # Get series information from database.
        results = dblib.select(
            dbconfig,
            table='anime',
            fields=['status'],
            where_filter='id = %s',
            where_args=(id,),
        )
        status = list(results)[0][0]
        # If series is not currently watching, mark for removal.
        if status != 'watching':
            to_delete.append(id)
    # Do removal
    if to_delete:
        for id in to_delete:
            del series[id]
        config['watch']['series'] = series
        config.save()


def _match_series_files(series_info, files):
    """Match series files.

    Use series information to associate with the given list of files.

    """
    series_files = [[id, pattern, name, ep_watched, list()]
                    for id, pattern, name, ep_watched in series_info]
    for filename in files:
        for _, pattern, _, ep_watched, matched_files in series_files:
            match = pattern.match(filename)
            if match:
                # Even if we match a file, we still check the episode number.
                # If it has already been watched, remove the file and don't add
                # it.
                if int(match.group('ep')) <= ep_watched:
                    os.remove(filename)
                    msg = 'Removed {} because it has already been watched.'
                    _LOGGER.info(msg.format(filename))
                else:
                    matched_files.append(filename)
                break
    return [[id, name, ep_watched, matched_files]
            for id, _, name, ep_watched, matched_files in series_files]


def main(args):
    """Entry point."""

    config = args.config

    dbconfig = config['db_args']
    playerconfig = config['watch']['player']

    while True:
        # Load series information.
        series_info = _fetch_series_info(config)

        # Use series information to search current directory for files and
        # match them with a series.
        files = sorted(os.listdir('.'))
        series_files = _match_series_files(series_info, files)

        # Choose series to watch.
        msg = "({}) {} (cur. ep. {}, {} eps.)"
        i = inputlib.get_choice(
            [msg.format(id, name, ep_watched, len(matched_files))
             for id, name, ep_watched, matched_files in series_files]
        )

        # XXX Left off here

        # Play episodes in order.
        # After each episode, bump or delete?

        # XXX Old stuff follows

        # Choose file
        files = os.listdir('.')
        files = [file for file in files
                 if os.path.splitext(file)[1] in ('.mp4', '.mkv')]
        if not files:
            return
        files = sorted(files)
        i = inputlib.get_choice(files)

        # Process file
        filename = files[i]
        play(playerconfig, filename)

        while True:
            try:
                info = get_info(filename, args.config['file_dir'])
            except ValueError:
                input('Match not found.  Press Return once problem is fixed.')
            else:
                break
        dst_path = os.path.join(info.filing, filename)

        print('Info found: {!r}'.format(info))
        i = input('Abort which? [rb] ')
        i = set(i)
        if 'r' not in i:
            os.rename(filename, dst_path)
            print('Refiled.')
            _LOGGER.info('Moved %s to %s', filename, dst_path)
        if 'b' not in i:
            print('>>>> ' + filename)
            ibump(dbconfig, info.name)
