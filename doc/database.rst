Database format
===============

All of Animanager's data is stored in a SQLite3 database.  You can do any manual
adjustments, complex queries, or batch transformations of data directly on the
database file using the SQLite3 command line or a SQLite3 browser such as
sqlitebrowser.

Make sure to enable foreign key support when working with the database::

  PRAGMA foreign_keys = ON

Here is a description of the columns in the ``anime`` table:

id
  Internal ID.

name
  Name of series.

type
  Type of series.  Can be TV, Movie, Special, OVA, ONA, or Music.  Check the
  ``anime_types`` table.

ep_watched
  Number of episodes currently watched.

ep_total
  Total number of episodes.  Can be NULL.

status
  Your current watching status.  Can be complete, on hold, dropped, watching,
  or plan to watch.  Check the ``anime_statuses`` table.

date_started
  Date you started watching, in this format: "2015-01-20".

date_finished
  Date you finished watching, in this format: "2015-01-20".

animedb_id
  This is the internal ID used by MAL for this series.


Manga support
-------------

Note that the database contains everything needed for manga as well.  While
Animanager does not currently support manga tracking, the database does support
manga.  You can manually enter information for manga until such time Animanager
receives manga support.

More information
----------------

For even more detailed information, check the schema of the database, including
the triggers and various type constraints on the columns.
