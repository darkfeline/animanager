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

from abc import abstractmethod

from .base import BaseDatabase


class BaseCacheTableMixin(BaseDatabase):

    """Interface for cache table mixins.

    Subclasses should implement setup_cache_tables() and cleanup_cache_tables()
    to set up and clean up their cache tables, respectively.  These should call
    super() before doing anything.  Thus, cache table mixins will be handled in
    reverse MRO order.

    Subclasses may define a dispatcher property, which returns a subclass of
    BaseDispatcher.  Dispatchers may define methods for performing operations
    solely on the cache tables of the parent cache table mixin.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_cache_tables()

    @abstractmethod
    def setup_cache_tables(self):
        pass

    @abstractmethod
    def cleanup_cache_tables(self):
        pass


class BaseDispatcher:

    """Base class for dispatchers for BaseCacheTableMixin subclasses."""

    __slots__ = ('cnx',)

    def __init__(self, parent):
        self.cnx = parent.cnx
