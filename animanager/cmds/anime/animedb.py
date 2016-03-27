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

import logging
from textwrap import dedent
from typing import Any, Dict, List

from tabulate import tabulate

from animanager.cmd import compile_sql_query
from animanager.cmd import CmdMixinMeta
from animanager.cmd import ArgumentParser

from animanager.date import fromtimestamp
from animanager.files import find_files
from animanager.files import AnimeFiles, is_video

logger = logging.getLogger(__name__)


class AnimeDBCmdMixin(metaclass=CmdMixinMeta):

    parser_search = ArgumentParser()
    parser_search.add_argument(
        '-w', '--watching', action='store_true',
        help='Limit to registered anime.',
    )
    parser_search.add_query()

    alias_s = 'search'

    def do_search(self, args):
        """Search Animanager database."""

        where_queries = []  # type: List[str]
        params = {}  # type: Dict[str, Any]
        if args.watching:
            where_queries.append('regexp IS NOT NULL')
        if args.query:
            where_queries.append('title LIKE :title')
            params['title'] = compile_sql_query(args.query)
        if not where_queries:
            print('Must include at least one filter.')
            return
        where_query = ' AND '.join(where_queries)

        results = list()
        all_files = find_files(self.config.anime.watchdir, is_video)
        for anime in self.animedb.select(where_query, params):
            anime_files = AnimeFiles(anime.regexp)
            anime_files.maybe_add_iter(all_files)
            logger.debug('Found files %s', anime_files.by_episode)
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
        Complete: {}""")

    parser_show = ArgumentParser()
    parser_show.add_aid()
    parser_show.add_argument('-e', '--show-episodes', action='store_true')

    alias_sh = 'show'

    def do_show(self, args):
        """Show anime data."""
        aid = self.get_aid(args.aid, default_key='db')
        anime = self.animedb.lookup(aid, args.show_episodes)

        complete_string = 'yes' if anime.complete else 'no'
        print(self._SHOW_MSG.format(
            anime.aid,
            anime.title,
            anime.type,
            anime.watched_episodes,
            anime.episodecount,
            fromtimestamp(anime.startdate) if anime.startdate else 'N/A',
            fromtimestamp(anime.enddate) if anime.enddate else 'N/A',
            complete_string,
        ))
        if anime.regexp:
            print('Watching regexp: {}'.format(anime.regexp))
        if anime.episodes:
            episodes = sorted(anime.episodes, key=lambda x: (x.type, x.number))
            print('\n', tabulate(
                (
                    (
                        self.animedb.get_epno(episode), episode.title,
                        episode.length, 'yes' if episode.user_watched else '')
                    for episode in episodes),
                headers=['Number', 'Title', 'min', 'Watched'],
            ))

    parser_bump = ArgumentParser()
    parser_bump.add_aid()

    alias_b = 'bump'

    def do_bump(self, args):
        """Bump anime."""
        aid = self.get_aid(args.aid, default_key='db')
        self.animedb.bump(aid)