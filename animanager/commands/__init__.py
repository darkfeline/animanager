# Copyright (C) 2018  Allen Li
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

from .add import command as add
from .addrule import command as addrule
from .asearch import command as asearch
from .deleterule import command as deleterule
from .gpl import command as gpl
from .help import command as help
from .purgecache import command as purgecache
from .register import command as register
from .rules import command as rules
from .unregister import command as unregister
from .update import command as update
from .watch import command as watch


def quit(cmd, args):
    return True
