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

from . import argparse
from .registry import Registry


registry = Registry()


@registry.register('do_asearch')
@registry.register('do_as')
@argparse.re_query_parser.parsing
def do_asearch(self, args):
    """Search AniDB."""
    results = self.searchdb.search(args.query)
    results = [(anime.aid, anime.main_title) for anime in results]
    self.results['anidb'].set(results)
    self.results['anidb'].print()


@registry.register('help_as')
def help_as(self):
    print('Alias for asearch.')


_ASHOW_MSG = dedent("""\
    AID: {}
    Title: {}
    Type: {}
    Episodes: {}
    Start date: {}
    End date: {}\n""")

@registry.register('do_ashow')
@registry.register('do_ash')
@argparse.aid_parser.parsing
def do_ashow(self, args):
    """Show information about anime in AniDB."""
    aid = self.get_aid(args.aid, default_key='anidb')
    anime = self.anidb.lookup(aid)
    print(_ASHOW_MSG.format(
        anime.aid,
        anime.title,
        anime.type,
        anime.episodecount,
        anime.startdate,
        anime.enddate,
    ))
    print(tabulate(
        (
            (episode.epno, episode.title, episode.length)
            for episode in sorted(
                    anime.episodes,
                    key=lambda x: (x.type, x.number))),
        headers=['Number', 'Title', 'min'],
    ))


@registry.register('help_ash')
def help_ash(self):
    print('Alias for ashow.')


@registry.register('do_add')
@registry.register('do_a')
@argparse.aid_parser.parsing
def do_add(self, args):
    """Add an anime or update an existing anime."""
    aid = self.get_aid(args.aid, default_key='anidb')
    anime = self.anidb.lookup(aid)
    self.animedb.add(anime)


@registry.register('help_a')
def help_a(self):
    print('Alias for add.')
