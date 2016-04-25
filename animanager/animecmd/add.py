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

from animanager.anidb import request_anime
from animanager.cmd import ArgumentParser, Command
from animanager.db import query

parser = ArgumentParser(prog='add')
parser.add_argument('aid')

def func(cmd, args):
    """Add an anime from an AniDB search."""
    aid = cmd.results.parse_aid(args.aid, default_key='anidb')
    anime = request_anime(aid)
    query.update.add(cmd.db, anime)

command = Command(parser, func)
