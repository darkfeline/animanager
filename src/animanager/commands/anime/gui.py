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

"""
Automated anime watching and tracking script.
"""

import logging

from gi.repository import Gtk

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'gui',
        description='Start Animanager GUI.',
        help='Start Animanager GUI.',
    )
    parser.set_defaults(func=main)


class MainWindow(Gtk.Window):

    def __init__(self, config, db):
        Gtk.Window.__init__(self, title="Animanager")

        self.config = config
        self.db = db

        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(mainbox)

        self.store = Gtk.ListStore(str)
        self.view = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        self.view.append_column(column)
        mainbox.pack_start(self.view, True, True, 2)

        subbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mainbox.pack_start(subbox, True, True, 2)

        self.button = Gtk.Button(label="Reload")
        self.button.connect("clicked", self.load_files_to_watch())
        subbox.pack_start(self.button, True, True, 2)

        self.button = Gtk.Button(label="Watch")
        self.button.connect("clicked", self.watch_show())
        subbox.pack_start(self.button, True, True, 2)

    def load_files_to_watch(self, widget):
        # Load series information.
        series_list = _load_series_info(db, config)

        # Use series information to search current directory for files and
        # match them with a series.
        files = [file
                for file in sorted(config['watch'].getpath('directory'))
                if _file_ext(file) in _VIDEO_EXT]
        series_list = _load_files(series_list, files)
        del files

    def watch_show(self, widget):
        pass


def main(args):
    """Entry function."""
    win = MainWindow(args.config, args.db)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
