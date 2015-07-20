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

"""Tools for getting input"""

import cmd


class ChoiceCmd(cmd.Cmd):

    intro = "Type ? for help."
    prompt = "$"

    def __init__(self, choices, default=-1):
        self.original_choices = choices
        self.choice = default

    def help_general(self):
        print("Type the number of a choice or use a specific command.")

    def preloop(self):
        # Initialize choices and print
        self.do_r()
        self.do_p()

    def do_r(self):
        """Reset choices."""
        self.choices = list(enumerate(self.original_chocies))

    def do_f(self, arg):
        """Filter choice set."""
        self.choices = [(i, choice)
                        for i, choice in self.choices
                        if arg in choice]

    def do_p(self):
        """Print choices."""
        for i, choice in self.choices:
            print("{}: {}".format(i, choice))

    def emptyline(self):
        """Use default choice."""
        return True

    def default(self, line):
        """Pick a choice."""
        try:
            filtered_i = int(line)
        except ValueError:
            print('Invalid pick.')
        else:
            real_i = self.choices[filtered_i][1]
            self.choice = real_i
            return True


def get_choice(choices, default=-1):
    """Prompt for user to pick a choice.

    Args:
        choices: A list of choices strings.

    Returns:
        An int index of the given choice: choices[i].

    """
    cmd_interp = ChoiceCmd(choices, default)
    cmd_interp.cmdloop()
    return cmd_interp.choice


def get_yn(prompt, default=True):
    """Prompt user for a binary yes/no choice."""
    if default:
        prompt = prompt + ' [Y/n]'
    else:
        prompt = prompt + ' [y/N]'
    user_input = input(prompt)
    # If the default is yes/true, return true as long as the input is not no.
    # if the default is no, return no as long as the input is not yes.
    if default:
        return user_input.lower() not in ('n', 'no')
    else:
        return user_input.lower() in ('y', 'yes')
