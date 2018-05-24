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

from tabulate import tabulate

from animanager.cmdlib import ArgumentParser
from animanager import datets
from animanager.db import query
from animanager.db.query.eptype import EpisodeTypes


def command(state, args):
    """Show anime data."""
    args = parser.parse_args(args[1:])
    aid = state.results.parse_aid(args.aid, default_key='db')
    anime = query.select.lookup(state.db, aid, episode_fields=args.episode_fields)

    complete_string = 'yes' if anime.complete else 'no'
    print(SHOW_MSG.format(
        anime.aid,
        anime.title,
        anime.type,
        anime.watched_episodes,
        anime.episodecount,
        datets.to_date(anime.startdate) if anime.startdate else 'N/A',
        datets.to_date(anime.enddate) if anime.enddate else 'N/A',
        complete_string,
    ))
    if anime.regexp:
        print('Watching regexp: {}'.format(anime.regexp))
    if hasattr(anime, 'episodes'):
        episodes = sorted(anime.episodes, key=lambda x: (x.type, x.number))
        print('\n', tabulate(
            (
                (
                    EpisodeTypes.from_db(state.db).get_epno(episode),
                    episode.title,
                    episode.length,
                    'yes' if episode.user_watched else '',
                )
                for episode in episodes
            ),
            headers=['Number', 'Title', 'min', 'Watched'],
        ))


SHOW_MSG = """\
AID: {}
Title: {}
Type: {}
Episodes: {}/{}
Start date: {}
End date: {}
Complete: {}"""

parser = ArgumentParser(prog='show')
parser.add_argument('aid')
parser.add_argument(
    '-e', '--show-episodes',
    default=(), const=query.select.ALL, action='store_const',
    dest='episode_fields',
)
