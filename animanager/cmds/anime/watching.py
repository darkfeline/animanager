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

from animanager.cmd import ArgumentParser, CmdMixinMeta
from animanager.files.abc import BaseAnimeFiles


class WatchingCmdMixin(metaclass=CmdMixinMeta):

    parser_register = ArgumentParser()
    parser_register.add_aid()
    parser_register.add_argument('query', nargs=REMAINDER)

    alias_r = 'register'

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

    parser = ArgumentParser()
    parser.add_aid()

    alias_ur = 'unregister'

    def do_unregister(self, args):
        """Unregister watching regexp for an anime."""
        aid = self.get_aid(args.aid, default_key='db')
        self.animedb.delete_regexp(aid)

    parser_add_rule = ArgumentParser()
    parser_add_rule.add_argument('regexp')
    parser_add_rule.add_argument('priority', nargs='?', default=None, type=int)

    def do_add_rule(self, args):
        """Add a priority rule for files."""
        row_id = self.animedb.add_priority_rule(args.regexp, args.priority)
        del self.file_picker
        print('Added rule {}'.format(row_id))

    def do_rules(self, args):
        """List file priority rules."""
        rules = self.animedb.priority_rules
        print(tabulate(rules, headers=['ID', 'Regexp', 'Priority']))

    parser_delete_rule = ArgumentParser()
    parser_delete_rule.add_argument('id', type=int)

    def do_delete_rule(self, args):
        """List file priority rules."""
        self.animedb.delete_priority_rule(args.id)
        del self.file_picker

    parser_watch = ArgumentParser()
    parser_watch.add_aid()
    parser_watch.add_argument('episode', nargs='?', default=None, type=int)

    alias_w = 'watch'

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

        if not files:
            print('No files.')
            return

        file = self.file_picker.pick(files)
        subprocess.call(self.config.anime.player_args + [file])
        if episode == anime.watched_episodes + 1:
            user_input = input('Bump? [Yn]')
            if user_input.lower() in ('n', 'no'):
                print('Not bumped.')
            else:
                self.animedb.bump(aid)
                print('Bumped.')
