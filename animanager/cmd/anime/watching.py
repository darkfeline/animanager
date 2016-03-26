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
import subprocess
from argparse import REMAINDER

from tabulate import tabulate

from animanager.files.anime import BaseAnimeFiles
from animanager.registry.cmd import CmdRegistry

from .argparse import ArgumentParser

registry = CmdRegistry()


_parser = ArgumentParser(prog='register')
_parser.add_aid()
_parser.add_argument('query', nargs=REMAINDER)

@registry.register_alias('r')
@registry.register_command('register', _parser)
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


_parser = ArgumentParser(prog='unregister')
_parser.add_aid()

@registry.register_alias('ur')
@registry.register_command('unregister', _parser)
def do_unregister(self, args):
    """Unregister watching regexp for an anime."""
    aid = self.get_aid(args.aid, default_key='db')
    self.animedb.delete_regexp(aid)


_parser = ArgumentParser(prog='add_rule')
_parser.add_argument('regexp')
_parser.add_argument('priority', nargs='?', default=None, type=int)

@registry.register_command('add_rule', _parser)
def do_add_rule(self, args):
    """Add a priority rule for files."""
    row_id = self.animedb.add_priority_rule(args.regexp, args.priority)
    del self.file_picker
    print('Added rule {}'.format(row_id))


_parser = ArgumentParser(prog='rules')

@registry.register_command('rules', _parser)
def do_rules(self, args):
    """List file priority rules."""
    rules = self.animedb.priority_rules
    print(tabulate(rules, headers=['ID', 'Regexp', 'Priority']))


_parser = ArgumentParser(prog='delete_rule')
_parser.add_argument('id', type=int)

@registry.register_command('delete_rule', _parser)
def do_delete_rule(self, args):
    """List file priority rules."""
    self.animedb.delete_priority_rule(args.id)
    del self.file_picker


_parser = ArgumentParser(prog='watch')
_parser.add_aid()
_parser.add_argument('episode', nargs='?', default=None, type=int)

@registry.register_alias('w')
@registry.register_command('watch', _parser)
def do_watch(self, args):
    """Watch an anime."""
    aid = self.get_aid(args.aid, default_key='db')
    anime = self.animedb.lookup(aid)
    anime_files = self.animedb.get_files(aid)  # type: BaseAnimeFiles
    if args.episode is None:
        episode = anime.watched_episodes + 1  # type: int
    else:
        episode = args.episode  # type: int
    files = anime_files.get_episode(episode)

    file = self.file_picker.pick(files)

    subprocess.call(self.config.anime.player_args + [file])
    user_input = input('Bump? [Yn]')
    if user_input.lower() in ('n', 'no'):
        print('Not bumped.')
    else:
        self.animedb.bump(aid)
        print('Bumped.')
