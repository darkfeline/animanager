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

from animanager.cmd import ArgumentParser, CmdMixinMeta, compile_re_query


class AniDBCmdMixin(metaclass=CmdMixinMeta):

    parser_asearch = ArgumentParser()
    parser_asearch.add_query()

    alias_as = 'asearch'

    def do_asearch(self, args):
        """Search AniDB."""
        if not args.query:
            print('Must supply query.')
            return
        query = compile_re_query(args.query)
        results = self.searchdb.search(query)
        results = [(anime.aid, anime.main_title) for anime in results]
        self.results['anidb'].set(results)
        self.results['anidb'].print()

    parser_add = ArgumentParser()
    parser_add.add_aid()

    alias_a = 'add'

    def do_add(self, args):
        """Add an anime from an AniDB search."""
        aid = self.get_aid(args.aid, default_key='anidb')
        anime = self.anidb.lookup(aid)
        self.animedb.add(anime)

    parser_update = ArgumentParser()
    parser_update.add_aid()

    alias_u = 'update'

    def do_update(self, args):
        """Update an existing anime from a local database search."""
        aid = self.get_aid(args.aid, default_key='db')
        anime = self.anidb.lookup(aid)
        self.animedb.add(anime)
