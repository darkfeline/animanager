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

import logging

from animanager import mysqllib

logger = logging.getLogger(__name__)

statuses = ['plan to watch', 'watching', 'complete', 'dropped', 'on hold']
output_template = """Watching: {watching}
Complete: {complete}
On Hold: {on hold}
Dropped: {dropped}
Plan to Watch: {plan to watch}
Total: {total}"""


def main(args):
    config = args.config
    counts = {}
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute('SELECT count(*) FROM anime')
        counts['total'] = cur.fetchone()[0]
        query = 'SELECT count(*) FROM anime WHERE status=%s'
        for x in statuses:
            cur.execute(query, (x,))
            counts[x] = cur.fetchone()[0]
        print(output_template.format(**counts))
