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

import subprocess

from animanager.cmd import ArgumentParser, Command
from animanager.db import query

parser = ArgumentParser(prog='watch')
parser.add_argument('aid')
parser.add_argument('episode', nargs='?', default=None, type=int)


def func(cmd, args):
    """Watch an anime."""
    aid = cmd.results.parse_aid(args.aid, default_key='db')
    anime = query.select.lookup(cmd.db, aid)
    if args.episode is None:
        episode = anime.watched_episodes + 1
    else:
        episode = args.episode
    anime_files = query.files.get_files(cmd.db, aid)
    files = anime_files[episode]

    if not files:
        print('No files.')
        return

    file = cmd.file_picker.pick(files)
    ret = subprocess.call(cmd.config.anime.player_args + [file])
    if ret == 0 and episode == anime.watched_episodes + 1:
        user_input = input('Bump? [Yn]')
        if user_input.lower() in ('n', 'no'):
            print('Not bumped.')
        else:
            query.update.bump(cmd.db, aid)
            print('Bumped.')

command = Command(parser, func)
