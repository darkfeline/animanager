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

import re
import shlex
import subprocess
from argparse import REMAINDER

from animanager.registry import CmdRegistry

from .argparse import ArgumentParser, aid_parser

registry = CmdRegistry()


_register_parser = ArgumentParser()
_register_parser.add_aid()
_register_parser.add_argument('query', nargs=REMAINDER)

@registry.register_alias('r')
@registry.register_do('register')
@_register_parser.parsing
def do_register(self, args):
    """Register watching regexp for an anime."""
    aid = self.get_aid(args.aid, default_key='db')
    if args.query:
        # Use regexp provided by user.
        pattern = '.*'.join(args.query)
    else:
        # Make default regexp.
        title = self.animedb.lookup_title(aid)
        # Replace non-word, non-whitespace with whitespace.
        pattern = re.sub(r'[^\w\s]', ' ', title)
        # Split on whitespace and join with wildcard regexp.
        pattern = '.*'.join(re.escape(x) for x in pattern.split())
        # Append episode matching pattern.
        pattern = '.*?'.join((
            pattern,
            r'\b(?P<ep>[0-9]+)(v[0-9]+)?',
        ))
    self.animedb.set_regexp(aid, pattern)


@registry.register_alias('ur')
@registry.register_do('unregister')
@aid_parser.parsing
def do_unregister(self, args):
    """Unregister watching regexp for an anime."""
    aid = self.get_aid(args.aid, default_key='db')
    self.animedb.delete_regexp(aid)


_watch_parser = ArgumentParser()
_watch_parser.add_aid()
_watch_parser.add_argument('episode', default=None, type=int)


@registry.register_alias('w')
@registry.register_do('watch')
@_watch_parser.parsing
def do_watch(self, args):
    """Watch an anime."""
    aid = self.get_aid(args.aid, default_key='db')
    anime = self.animdb.lookup(aid)
    anime_files = self.animedb.get_files(aid)
    if args.episode is None:
        episode = anime.watched_episodes + 1  # type: int
    else:
        episode = args.episode  # type: int
    player = self.config.anime.player
    subprocess.call(shlex.split(player) + [])
    raise NotImplementedError
    # XXX get watching shows
    # XXX find files
    # XXX match rules
    # XXX play file
    # XXX bump

def _watch_list_all(self):
    # Find files.
    watchdir = self.config.anime.watchdir
    files = self._find_files(watchdir)

    # Associate files with watching anime.
    watching_list = self.animedb.get_watching()
    anime_files = dict((anime.aid, defaultdict(list)) for anime in watching_list)
    for filename in files:
        for anime in watching_list:
            match = anime.regexp.search(os.path.basename(filename))
            if match:
                try:
                    ep = int(match.group('ep'))
                except ValueError:
                    logger.error(
                        'Invalid episode matched using %s for %s',
                        anime.title, filename)
                    continue
                anime_files[anime.aid][ep].append(files)
                break

    # Print
    pass  # XXX