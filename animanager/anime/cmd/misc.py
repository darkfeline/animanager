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

from animanager.registry import Registry


registry = Registry()


@registry.register_alias('q')
@registry.register_do('quit')
def do_quit(self, arg):
    """Quit."""
    return True


@registry.register_do('purgecache')
def do_purgecache(self, arg):
    """Purge cache tables."""
    self.animedb.cleanup_cache_tables()
    self.animedb.setup_cache_tables()
