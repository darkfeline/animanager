Animanager Migration
====================

This is Animanager release 0.8.1.

The sole purpose of this release is for database migration to 0.9.0.  Animanager
0.9.0 is completely rewritten to fix many problems, including the lack of
automated database migrations.  However, in order to move on, an involved manual
migration is needed.  Tools to help you can be found in the `migration-tools`
directory.

Animanager 0.9.0 uses AniDB instead of MyAnimeList.  Mapping MyAnimeList IDs to
AniDB IDs must be done manually.

Backing up your database before each step is recommended.

Create a new column in the `anime` database.  You can use the included
`add-col.sql` script:

    $ sqlite3 database.db
    sqlite> .read add-col.sql

Now you must manually fill in the AniDB IDs.  The site is here:
<http://anidb.net/>.  Setting the IDs can be done with a SQLite tool like
sqlitebrowser.

There are some tools included to avoid getting banned from overusing the
website.  The `search` subdirectory contains a search script.  Download the list
of titles from here: <http://wiki.anidb.net/w/API#Anime_Titles>  Save the XML
version as `anime-titles.xml` in the `search` subdirectory.  Run:

    $ python3 search.py terms to search

There may be some anime that do not have a clean mapping from MyAnimeList IDs to
AniDB IDs.  Set these to NULL.

Next, you'll need to fetch data from AniDB to populate the new database.
Depending on the size of your current database, this may take a large amount of
time if you want to avoid getting banned.

Edit `paths.py` and set `NEW` to the path to the new database and `OLD` to the
path of your current database.

Run `fetch.py`:

    $ python3 fetch.py

Again, this may take a lot of time.  Do not remove the sleep call unless you
want to get banned or you have a very small database.

Finally, use `manual.py` to dump those shows that could not be migrated
automatically:

    $ python3 manual.py

These will need to be re-added using Animanager 0.9.0.  OVAs are currently not
really supported, due to how AniDB organizes them compared to MyAnimeList.
Their episodes can be set to watched manually if you wish to do so.

Store this list of unmigrated anime and the old database somewhere for
safekeeping.
