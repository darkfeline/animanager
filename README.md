# animanager

Personal anime database management tool.

## Dependencies

* Python 3
* [tabulate][1]

[1]: https://pypi.python.org/pypi/tabulate

## Installation

    $ python setup.py install

or

    $ python setup.py install --user

## Configuration/Setup

Copy the included configuration file `config.ini` to `~/.animanager/config.ini`.

Load the included database schema `schema.sql` into a SQLite3 database file at
`~/.animanager/database.db`:

    $ sqlite3 ~/.animanager/database.db '.read schema.sql'
