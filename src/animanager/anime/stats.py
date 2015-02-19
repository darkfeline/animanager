# Copyright (C) 2015  Allen Li
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

"""Stats command."""

from animanager import dblib

_STATUSES = ['plan to watch', 'watching', 'complete', 'dropped', 'on hold']
_OUTPUT_TEMPLATE = """Watching: {watching}
Complete: {complete}
On Hold: {on hold}
Dropped: {dropped}
Plan to Watch: {plan to watch}
Total: {total}
Episodes watched: {ep_watched}"""


def main(args):
    """Stats command."""
    config = args.config
    counts = {}
    with dblib.connect(config["db_args"]) as cur:
        cur.execute('SELECT count(*) FROM anime')
        counts['total'] = cur.fetchone()[0]
        query = 'SELECT count(*) FROM anime WHERE status=%s'
        for status in _STATUSES:
            cur.execute(query, (status,))
            counts[status] = cur.fetchone()[0]
        cur.execute('SELECT SUM(ep_watched) FROM anime')
        counts['ep_watched'] = cur.fetchone()[0]
        # pylint: disable=star-args
        print(_OUTPUT_TEMPLATE.format(**counts))
