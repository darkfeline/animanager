Installation and configuration
==============================

Dependencies
------------

You need the following dependencies to run Animanager

- Python 3
- `tabulate`_

.. _tabulate: https://pypi.python.org/pypi/tabulate

Python 3 is needed to run Animanager.  tabulate is needed for printing pretty
tables (e.g., ``anime search``).

tabulate can be installed manually with pip::

  $ pip3 install tabulate

Installation
------------

Animanager can be installed manually::

  # python3 setup.py install

or::

  $ python3 setup.py install --user


Database setup
--------------

Load the included database schema ``schema.sql`` into a SQLite3 database file at
``~/.animanager/database.db``::

  $ sqlite3 ~/.animanager/database.db '.read schema.sql'

Configuration
-------------

Copy the included configuration file ``config.ini`` to
``~/.animanager/config.ini``.  Read the file and edit it accordingly.

You will definitely need to edit the credentials for logging into `MyAnimeList`_
(MAL).  This is used to pull information using MAL's API.

.. _MyAnimeList: http://myanimelist.net/

You may want to edit the ``player`` line to configure which video player to
use.  Examples::

  player = mpv --fullscreen
  player = mplayer

The ``[series]`` section is described in detail elsewhere; you do not need to
touch it right now.
