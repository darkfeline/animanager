# Copyright (C) 2015-2016  Allen Li
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

import os
from typing import Iterable


def find_files(dirpath: str) -> Iterable[str]:
    """Find files recursively.

    Returns a generator that yields paths in no particular order.

    """
    for dirpath, dirnames, filenames in os.walk(dirpath, topdown=True,
                                                followlinks=True):
        if os.path.basename(dirpath).startswith('.'):
            del dirnames[:]
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def is_video(filepath) -> bool:
    """Check filename extension to see if it's a video file."""
    if os.path.exists(filepath):  # Could be broken symlink
        extension = os.path.splitext(filepath)[1]
        return extension in ('.mkv', '.mp4', '.avi')
    else:
        return False
