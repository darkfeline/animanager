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

from animanager.argparse import compile_re_query
from animanager.registry.cmd import CmdRegistry

from .argparse import ArgumentParser

registry = CmdRegistry()


_parser = ArgumentParser(prog='asearch')
_parser.add_query()

@registry.register_alias('as')
@registry.register_command('asearch', _parser)
def do_asearch(self, args):
    """Search AniDB."""
    query = compile_re_query(args.query)
    results = self.searchdb.search(query)
    results = [(anime.aid, anime.main_title) for anime in results]
    self.results['anidb'].set(results)
    self.results['anidb'].print()


_parser = ArgumentParser(prog='add')
_parser.add_aid()

@registry.register_alias('a')
@registry.register_command('add', _parser)
def do_add(self, args):
    """Add an anime or update an existing anime."""
    aid = self.get_aid(args.aid, default_key='anidb')
    anime = self.anidb.lookup(aid)
    self.animedb.add(anime)
