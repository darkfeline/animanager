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

import logging
import os
import subprocess

from animanager import inputlib

from .bump import ibump

PLAYER = 'mpv'
VID_DIR = os.path.join(os.environ['HOME'], 'bibliotheca', 'vid')
_LOGGER = logging.getLogger(__name__)


def match_dir(filename, directory):
    """Match given filename with subdirectory in given directory."""
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)) and name in filename:
            return name
    raise ValueError("Match not found.")


def process(dbconfig, filename):
    """Do watching process for file."""
    # Play
    subprocess.call([PLAYER, filename])
    # Refile
    dst_dir = match_dir(filename, VID_DIR)
    dst_path = os.path.join(VID_DIR, dst_dir, os.path.basename(filename))
    os.rename(filename, dst_path)
    _LOGGER.info('Moved %s to %s', filename, dst_path)
    print('>>>> ' + filename)
    i = input('Bump? [Y/n]')
    if i.lower() in ('n', 'no'):
        return
    ibump(dbconfig, dst_dir)


def main(args):
    """Entry point."""
    dbconfig = args.config['db_args']
    while True:
        files = os.listdir('.')
        files = [file for file in files
                 if os.path.splitext(file)[1] in ('.mp4', '.mkv')]
        if not files:
            return
        i = inputlib.get_choice(files)
        process(dbconfig, files[i])
        i = input('Quit? [y/N]')
        if i.lower() in ('y', 'yes'):
            return
