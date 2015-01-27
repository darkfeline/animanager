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

def get_choice(choices, default=-1):
    """Prompt for user to pick a choice.

    Args:
        choices: A list of choices strings.

    Returns:
        An int index of the given choice: choices[i].

    """
    for i, name in enumerate(choices):
        print("{}: {}".format(i, name))
    try:
        i = int(input("Pick [{}]: ".format(default)))
    except ValueError:
        i = default
    return i
