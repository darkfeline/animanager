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

from textwrap import dedent

from tabulate import tabulate

from animanager.argparse import compile_sql_query
from animanager.date import fromtimestamp
from animanager.files import find_files
from animanager.files.anime import AnimeFiles, is_video
from animanager.registry.cmd import CmdRegistry

from .argparse import ArgumentParser

registry = CmdRegistry()


_parser = ArgumentParser(prog='search')
_parser.add_query()

@registry.register_alias('s')
@registry.register_command('search', _parser)
def do_search(self, args):
    """Search Animanager database."""
    query = compile_sql_query(args.query)
    all_files = find_files(self.config.anime.watchdir, is_video)
    results = list()
    for anime in self.animedb.search(query):
        anime_files = AnimeFiles(anime.regexp)
        anime_files.maybe_add_iter(all_files)
        self.animedb.cache_files(anime.aid, anime_files)
        results.append((
            anime.aid, anime.title, anime.type,
            '{}/{}'.format(anime.watched_episodes, anime.episodecount),
            'yes' if anime.complete else '',
            anime_files.available_string(),
        ))
    self.results['db'].set(results)
    self.results['db'].print()


_SHOW_MSG = dedent("""\
    AID: {}
    Title: {}
    Type: {}
    Episodes: {}/{}
    Start date: {}
    End date: {}
    Complete: {}
    {}""")
_parser = ArgumentParser(prog='show')
_parser.add_aid()
_parser.add_argument('-e', '--show-episodes', action='store_true')

@registry.register_alias('sh')
@registry.register_command('show', _parser)
def do_show(self, args):
    """Show anime data."""
    aid = self.get_aid(args.aid, default_key='db')
    anime = self.animedb.lookup(aid, args.show_episodes)

    complete_string = 'yes' if anime.complete else 'no'
    if anime.regexp is None:
        regexp_string = ''
    else:
        regexp_string = 'Watching regexp: {}\n'.format(anime.regexp)
    print(_SHOW_MSG.format(
        anime.aid,
        anime.title,
        anime.type,
        anime.watched_episodes,
        anime.episodecount,
        fromtimestamp(anime.startdate) if anime.startdate else 'N/A',
        fromtimestamp(anime.enddate) if anime.enddate else 'N/A',
        complete_string,
        regexp_string,
    ))
    if anime.episodes:
        print(tabulate(
            (
                (
                    self.animedb.get_epno(episode), episode.title, episode.length,
                    'yes' if episode.user_watched else '')
                for episode in sorted(
                    anime.episodes,
                    key=lambda x: (x.type, x.number))
            ),
            headers=['Number', 'Title', 'min', 'Watched'],
        ))


_parser = ArgumentParser(prog='bump')
_parser.add_aid()

@registry.register_alias('b')
@registry.register_command('bump', _parser)
def do_bump(self, args):
    """Bump anime."""
    aid = self.get_aid(args.aid, default_key='db')
    self.animedb.bump(aid)
