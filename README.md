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
