animanager
==========

Website: https://darkfeline.github.io/animanager/

Personal anime database management tool.

Quick Install
-------------

    $ pip3 install --user animanager

I highly recommend that you read the documentation (see below).

Configuration/Setup
-------------------

Copy the included configuration file `config.ini` to `~/.animanager/config.ini`.

Load the included database schema `schema.sql` into a SQLite3 database file at
`~/.animanager/database.db`:

    $ sqlite3 ~/.animanager/database.db '.read schema.sql'

More information
----------------

See the documentation for more detailed information.  It can be found in the
`doc` directory, or online at [Read the Docs](http://animanager.readthedocs.org/).
