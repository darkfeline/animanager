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
Anime filer script.
"""

from collections import namedtuple
import json
import logging
import os
import subprocess

from animanager import inputlib

from .bump import ibump

PLAYER = 'mpv'
VID_DIR = os.path.join(os.environ['HOME'], 'bibliotheca', 'vid')
_LOGGER = logging.getLogger(__name__)
INFO_FILE = 'info.json'

MatchInfo = namedtuple('MatchInfo', ['name', 'matches', 'filing'])


def read_info_file(directory):
    """Try to read info file."""
    path = os.path.join(directory, INFO_FILE)
    if os.path.exists(path):
        with open(path) as file:
            return MatchInfo(filing=directory, **json.load(file))
    else:
        return None


def get_info(filename, directory):
    """Get info for filing and bumping a show.

    Args:
        filename: Filename.
        directory: Path to filing directory.

    """
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if not os.path.isdir(path):
            continue
        info = read_info_file(path)
        if info is None:
            info = MatchInfo(name, name, path)
        _LOGGER.debug('Info %r', info)
        if info.matches in filename:
            return info
    raise ValueError("Match not found.")


def play(filename):
    """Play video."""
    subprocess.call([PLAYER, filename])


def main(args):
    """Entry point."""
    dbconfig = args.config['db_args']
    while True:
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
        play(filename)

        info = get_info(filename, VID_DIR)
        dst_path = os.path.join(info.filing, filename)

        i = input('Abort which? [rb] ')
        i = set(i)
        if 'r' not in i:
            os.rename(filename, dst_path)
            print('Refiled.')
            _LOGGER.info('Moved %s to %s', filename, dst_path)
        if 'b' not in i:
            print('>>>> ' + filename)
            ibump(dbconfig, info.name)
