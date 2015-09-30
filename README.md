# animanager

Website: https://darkfeline.github.io/animanager/

Personal anime database management tool.

## Dependencies

* Python 3
* setuptools
* [tabulate][1]

[1]: https://pypi.python.org/pypi/tabulate

## Installation

    $ python3 setup.py install

or

    $ python3 setup.py install --user

## Configuration/Setup

Copy the included configuration file `config.ini` to `~/.animanager/config.ini`.

Load the included database schema `schema.sql` into a SQLite3 database file at
`~/.animanager/database.db`:

    $ sqlite3 ~/.animanager/database.db '.read schema.sql'

## More information

See the documentation for more detailed information.  It can be found in the
`doc` directory, or online at `Read the Docs
<http://animanager.readthedocs.org/>`_.
