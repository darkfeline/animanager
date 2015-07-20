# animanager

Personal anime database management tool.

## Dependencies

* Python 3
* [Python MySQL connector 1.0.12][2]

[2]: https://dev.mysql.com/downloads/connector/python/

## Configuration

You need to set up a config file.  The default path is `~/.animanager.json`.  The file
is in JSON format.

### Example config

    {
        "watch": {
            "player": ["mpv"],
            "series": [
                [10, ".*Haruhi.*(?P<ep>[0-9]+)"],
            ],
        },
        "db_args": {
            "host": "localhost",
            "user": "anime",
            "passwd": "anime",
            "db": "anime",
            "charset": "utf8"
        },
        "mal_args": {
            "user": "haruhi",
            "passwd": "kyon"
        }
    }

### Top level keys

#### watch

These are used for configuring the `watch` command.

- player: The command line arguments used for launching a video player.
- series: A list of 2-tuples mapping an anime series ID to a regex for matching
  against the filenames of episodes of that series.  The match group named `ep`
  is used for the episode number.

#### player

What video player to use for `watch` command.  Pass a list of strings comprising
the separate command line arguments.

#### db_args

These are passed directly to the `connect()` function for MySQL.  See the
[official documentation][1] for details.

[1]: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysql-connector-connect.html

Here are some common arguments:

- host: Hostname of server
- user: MySQL user for access
- passwd: password for MySQL user
- db: Database name
- charset: Charset of database

#### mal_args

These are used for authenticating with MAL, for making queries against its API.

- user
- passwd

## Database configuration

The `db.sql` file is used for setting up the database.
