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
import subprocess
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from animanager import watchlib
from animanager import trashlib

_LOGGER = logging.getLogger(__name__)


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        'gui',
        description='Start Animanager GUI.',
        help='Start Animanager GUI.',
    )
    parser.set_defaults(func=main)


class YesNoDialog(Gtk.Dialog):

    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self, 'Select', parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK),
                            flags=Gtk.DialogFlags.MODAL)
        self.set_default_size(150, 100)
        parentbox = self.get_content_area()

        label = Gtk.Label(message)
        parentbox.add(label)

        self.show_all()


class SelectDialog(Gtk.Dialog):

    def __init__(self, parent, choices):
        Gtk.Dialog.__init__(self, 'Select', parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK),
                            flags=Gtk.DialogFlags.MODAL)
        self.set_default_size(150, 100)
        parentbox = self.get_content_area()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        parentbox.add(box)

        store = Gtk.ListStore(int, str)
        view = Gtk.TreeView(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Choice', renderer, text=1)
        view.append_column(column)
        box.pack_start(view, True, True, 2)

        select = view.get_selection()
        select.connect("changed", self._on_selection_changed)

        for i, x in enumerate(choices):
            store.append([i, x])

        self.show_all()

    def _on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selection = model[treeiter][0]


class MainWindow(Gtk.Window):

    def __init__(self, config, db):
        Gtk.Window.__init__(self, title="Animanager")

        self.config = config
        self.db = db

        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(mainbox)

        self.store = Gtk.ListStore(int, int, str, int, int, bool)
        view = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        for i, name in enumerate(['id', 'series', 'cur.', 'avail.',
                                  'missing?']):
            column = Gtk.TreeViewColumn(name, renderer, text=i+1)
            view.append_column(column)
            mainbox.pack_start(view, True, True, 2)

        select = view.get_selection()
        select.connect("changed", self._on_selection_changed)

        subbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mainbox.pack_start(subbox, True, True, 2)

        button = Gtk.Button(label="Reload")
        button.connect("clicked", self.load_files_to_watch)
        subbox.pack_start(button, True, True, 2)

        button = Gtk.Button(label="Watch")
        button.connect("clicked", self.watch_show)
        subbox.pack_start(button, True, True, 2)

        button = Gtk.Button(label="Bump")
        button.connect("clicked", self.bump_show)
        subbox.pack_start(button, True, True, 2)

        self.load_files_to_watch()

    def _on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selection = model[treeiter]

    def load_files_to_watch(self, widget=None):
        # Load series information.
        series_list = watchlib.load_series_info(self.db, self.config)

        # Use series information to search for files and
        # match them with a series.
        files = watchlib.find_files(self.config)
        series_list = watchlib.load_files(series_list, files)
        del files

        # Clean up unneeded files.
        unneeded = []
        for x in series_list:
            unneeded.extend(x.clean())
        for file in unneeded:
            trashlib.trash(self.config, file)
        # Remove series that no longer have any files.
        series_list = [x for x in series_list if x]

        self.series_list = series_list

    @property
    def series_list(self):
        return self._series_list

    @series_list.setter
    def series_list(self, value):
        self._series_list = value
        self._update_view()

    def _update_view(self):
        """Update GUI view using series_list."""
        self.store.clear()
        for i, info in enumerate(self.series_list):
            self.store.append([i, info.id, info.name, info.ep_watched,
                               len(info), not info.has_next()])

    def watch_show(self, widget=None):
        info = self.series_list[self.selection[0]]
        # Check if we have the next episode.
        if not info.has_next():
            return

        # Choose the file to play if there is more than one.
        files = info.peek()
        if len(files) > 1:
            dialog = SelectDialog(self, [os.path.basename(x) for x in files])
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.OK:
                i = dialog.selection
            else:
                return
            file = files[i]
        else:
            file = files[0]
        del files

        # Play the episode.
        subprocess.Popen(self.config['watch'].getargs('player') + [file])

    def bump_show(self, widget=None):
        info = self.series_list[self.selection[0]]

        # Check if we have the next episode.
        if not info.has_next():
            return

        self.db.bump(info.id)
        # Remove the episode from our list.
        old = info.pop()
        for file in old:
            trashlib.trash(self.config, file)

        # Filter out series that have no files.
        self.series_list = [x for x in self.series_list if x]


def main(args):
    """Entry function."""
    win = MainWindow(args.config, args.db)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
