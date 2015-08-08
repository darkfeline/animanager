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


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'clean',
        description='Clean up completed series from config.',
        help='Clean up completed series from config.',
    )
    parser.set_defaults(func=main)


def _filter_series(db, config):
    """Remove completed series from config file."""
    series = config['series']
    to_delete = []
    for id, _ in series.items():
        id = int(id)
        # Get series information from database.
        results = db.select(
            table='anime',
            fields=['status'],
            where_filter='id=?',
            where_args=(id,),
        )
        status = list(results)[0][0]
        if status == 'complete':
            to_delete.append(id)
    # Do removal
    if to_delete:
        for id in to_delete:
            config.unregister(id)
        config.save()


def main(args):
    _filter_series(args.db, args.config)
