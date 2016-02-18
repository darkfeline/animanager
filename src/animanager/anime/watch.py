# Copyright (C) 2015-2016  Allen Li
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
import subprocess
import shlex

from animanager import inputlib
from animanager import watchlib
from animanager import trashlib

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'watch',
        description='Automate watching episodes and updating counts',
        help='Automate watching episodes and updating counts',
    )
    parser.set_defaults(func=main)


def main(args):

    config = args.config
    db = args.db
    player_args = shlex.split(config['watch']['player'])

    # Load series information.
    series_list = watchlib.load_series_info(db, config)

    # Use series information to search for files and
    # match them with a series.
    files = watchlib.find_files(config)
    series_list = watchlib.load_files(series_list, files)
    del files

    # Clean up unneeded files.
    unneeded = []
    for x in series_list:
        unneeded.extend(x.clean())
    for file in unneeded:
        trashlib.trash(config, file)
    # Remove series that no longer have any files.
    series_list = [x for x in series_list if x]

    while series_list:
        # Choose series to watch.
        msg = "({id}) {name} (cur. {cur}, avail. {avail}){missing}"
        i = inputlib.get_choice(
            [msg.format(id=info.id, name=info.name, cur=info.ep_watched,
                        avail=len(info),
                        missing='' if info.has_next() else ' (missing)')
             for info in series_list],
            quit=True
        )
        if i is None:
            return

        info = series_list[i]

        # Check if we have the next episode.
        if not info.has_next():
            print('Next episode is missing.')
            continue

        # Choose the file to play if there is more than one.
        files = info.peek()
        if len(files) > 1:
            i = inputlib.get_choice(files)
            file = files[i]
            del files
        else:
            file = files[0]
        # Play the episode.
        subprocess.call(player_args + [file])
        del file

        if inputlib.get_yn('Bump?'):
            db.bump(info.id)
            # Remove the episode from our list.
            old = info.pop()
            for file in old:
                trashlib.trash(config, file)

        # Filter out series that have no files.
        series_list = [x for x in series_list if x]
