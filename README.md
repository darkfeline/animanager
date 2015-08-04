# animanager

Personal anime database management tool.

## Dependencies

* Python 3
* [Python MySQL connector 1.0.12][2]

[2]: https://dev.mysql.com/downloads/connector/python/

## Configuration/Setup

Copy the included configuration file `config.ini` to `~/.animanager/config.ini`.

Load the included database schema `schema.sql` into a SQLite3 database file at
`~/.animanager/database.db`:

    $ sqlite3 ~/.animanager/database.db '.read schema.sql'
