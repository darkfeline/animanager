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

import argparse
import re

from animanager.cmd import ArgumentParser, Command
from animanager.db import query

parser = ArgumentParser(prog='register')
parser.add_argument('aid')
parser.add_argument('query', nargs=argparse.REMAINDER)

def func(cmd, args):
    """Register watching regexp for an anime."""
    aid = cmd.results.parse_aid(args.aid, default_key='db')
    if args.query:
        # Use regexp provided by user.
        regexp = '.*'.join(args.query)
    else:
        # Make default regexp.
        title = query.select.lookup(cmd.db, aid, fields=['title']).title
        # Replace non-word, non-whitespace with whitespace.
        regexp = re.sub(r'[^\w\s]', ' ', title)
        # Split on whitespace and join with wildcard regexp.
        regexp = '.*?'.join(re.escape(x) for x in regexp.split())
        # Append episode matching regexp.
        regexp = '.*?'.join((
            regexp,
            r'\b(?P<ep>[0-9]+)(v[0-9]+)?',
        ))
    query.files.set_regexp(cmd.db, aid, regexp)

command = Command(parser, func)
