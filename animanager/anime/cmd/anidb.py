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
import re
import shlex

from tabulate import tabulate

from .registry import Registry


registry = Registry()


@registry.register('do_asearch')
@registry.register('do_as')
def do_asearch(self, arg):
    """Search AniDB."""
    if not arg:
        print('Missing query.')
        return
    query = re.compile('.*'.join(shlex.split(arg)), re.I)
    results = self.searchdb.search(query)
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
def do_ashow(self, arg):
    """Show information about anime in AniDB."""
    args = shlex.split(arg)
    if not args:
        print('Missing AID.')
        return
    aid = args.pop(0)
    aid = self.get_aid(aid, default_key='anidb')
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
def do_add(self, arg):
    """Add an anime or update an existing anime."""
    args = shlex.split(arg)
    if not args:
        print('Missing AID.')
        return
    aid = args.pop(0)
    aid = self.get_aid(aid, default_key='anidb')
    anime = self.anidb.lookup(aid)
    self.animedb.add(anime)


@registry.register('help_a')
def help_a(self):
    print('Alias for add.')
