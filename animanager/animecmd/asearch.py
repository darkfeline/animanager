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

import argparse

from animanager.cmd import ArgumentParser, Command, compile_re_query

parser = ArgumentParser(prog='asearch')
parser.add_argument('query', nargs=argparse.REMAINDER)

def func(cmd, args):
    """Search AniDB."""
    if not args.query:
        print('Must supply query.')
        return
    search_query = compile_re_query(args.query)
    results = cmd.titles.search(search_query)
    results = [(anime.aid, anime.main_title) for anime in results]
    cmd.results['anidb'].set(results)
    cmd.results['anidb'].print()

command = Command(parser, func)
