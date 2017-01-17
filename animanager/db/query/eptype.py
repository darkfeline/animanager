# Copyright (C) 2015-2017  Allen Li
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

"""Episode type queries."""

from collections import namedtuple
from typing import Iterable, Iterator

from animanager.sqlite import CachedView

from .collections import Episode

EpisodeType = namedtuple(
    'EpisodeType',
    ['id', 'name', 'prefix'])


def get_episode_types(db) -> Iterator[EpisodeType]:
    """Get all episode types."""
    cur = db.cursor()
    cur.execute('SELECT id, name, prefix FROM episode_type')
    for type_id, name, prefix in cur:
        yield EpisodeType(type_id, name, prefix)


def get_eptype(db, name):
    """Get episode type by name or id."""
    return EpisodeTypes.from_db(db)[name]


class EpisodeTypes(CachedView):

    """A class for storing all episode types.

    >>> x = EpisodeTypes([
    ...     EpisodeType(1, 'foo', 'F'),
    ...     EpisodeType(2, 'bar', 'B')])
    >>> x['foo']
    EpisodeType(id=1, name='foo', prefix='F')
    >>> x[2]
    EpisodeType(id=2, name='bar', prefix='B')
    >>> x[3]
    Traceback (most recent call last):
        ...
    KeyError: 3

    """

    def __init__(self, episode_types: Iterable[EpisodeType]):
        self.types = tuple(episode_types)
        self.by_id = {}
        self.by_name = {}
        for episode_type in self.types:
            self.by_id[episode_type.id] = episode_type
            self.by_name[episode_type.name] = episode_type

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.by_id[key]
        elif isinstance(key, str):
            return self.by_name[key]
        else:
            raise KeyError(key)

    @classmethod
    def _new_from_db(cls, db) -> 'EpisodeTypes':
        return cls(get_episode_types(db))

    def get_epno(self, episode: Episode):
        """Return epno for an Episode instance.

        epno is a string formatted with the episode number and type, e.g., S1,
        T2.

        >>> x = EpisodeTypes([EpisodeType(1, 'foo', 'F')])
        >>> ep = Episode(type=1, number=2)
        >>> x.get_epno(ep)
        'F2'

        """
        return '{}{}'.format(self[episode.type].prefix, episode.number)
