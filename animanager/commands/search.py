# Copyright (C) 2018  Allen Li
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
import logging
import os

from animanager.cmdlib import ArgumentParser
from animanager.db import query
from animanager.files import AnimeFiles

logger = logging.getLogger(__name__)


def command(state, args):
    """Search Animanager database."""

    args = parser.parse_args(args[1:])
    where_queries = []
    params = {}
    if args.watching or args.available:
        where_queries.append('regexp IS NOT NULL')
    if args.query:
        where_queries.append('title LIKE :title')
        params['title'] = _compile_sql_query(args.query)
    if not where_queries:
        print('Must include at least one filter.')
        return
    where_query = ' AND '.join(where_queries)
    logger.debug('Search where %s with params %s', where_query, params)

    results = list()
    all_files = [
        filename for filename in _find_files(state.config['anime'].getpath('watchdir'))
        if _is_video(filename)
    ]
    for anime in query.select.select(state.db, where_query, params):
        logger.debug('For anime %s with regexp %s', anime.aid, anime.regexp)
        if anime.regexp is not None:
            anime_files = AnimeFiles(anime.regexp, all_files)
            logger.debug('Found files %s', anime_files.filenames)
            query.files.cache_files(state.db, anime.aid, anime_files)
            available = anime_files.available_string(anime.watched_episodes)
        else:
            available = ''
        if not args.available or available:
            results.append((
                anime.aid, anime.title, anime.type,
                '{}/{}'.format(anime.watched_episodes, anime.episodecount),
                'yes' if anime.complete else '',
                available,
            ))
    state.results['db'].set(results)
    state.results['db'].print()


parser = ArgumentParser(prog='search')
parser.add_argument(
    '-w', '--watching', action='store_true',
    help='Limit to registered anime.',
)
parser.add_argument(
    '-a', '--available', action='store_true',
    help='Limit to anime with available episodes.  Implies --watching.',
)
parser.add_argument('query', nargs=argparse.REMAINDER)


def _is_video(filepath) -> bool:
    """Check filename extension to see if it's a video file."""
    if os.path.exists(filepath):  # Could be broken symlink
        extension = os.path.splitext(filepath)[1]
        return extension in ('.mkv', '.mp4', '.avi')
    else:
        return False


def _find_files(dirpath: str) -> 'Iterable[str]':
    """Find files recursively.

    Returns a generator that yields paths in no particular order.
    """
    for dirpath, dirnames, filenames in os.walk(dirpath, topdown=True,
                                                followlinks=True):
        if os.path.basename(dirpath).startswith('.'):
            del dirnames[:]
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def _compile_sql_query(args: 'Iterable[str]') -> str:
    return '%{}%'.format('%'.join(args))
