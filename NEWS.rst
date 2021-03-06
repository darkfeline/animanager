animanager Release Notes
========================

This project uses `semantic versioning <http://semver.org/>`_.

0.12.0 (2018-08-20)
-------------------

This is the last release of the Python version of Animanager (barring
bug fixes for bugs that prevent migration to the new version).

Future Animanager development will happen on the `Go version
<https://go.felesatra.moe/animanager>`_.

Added
^^^^^

Added ``fix`` command.  This command fixes certain issues caused by
caching for the schema up to v3 (the latest on the Python version).
Run this command before migrating to the Go version.  The Go version
will update the schema to v4 on the first run.

(It is fine to migrate to the Go version without running ``fix``.
However, this will leave database inconsistencies unfixed and purge
the cached data necessary for fixing these inconsistencies.)

Make sure to backup your database before running ``fix``.

またね

0.11.0 (2017-10-22)
-------------------

Added
^^^^^

- Added ``-i`` flag to ``update`` command.
- Added feature to use previous command when hitting Enter at a blank
  command line.
- Added ``reg`` and ``unreg`` aliases for ``register`` and ``unregister``.
- Added ``-w`` flag to ``update`` command.

Changed
^^^^^^^

- Don't offer to bump when video player exits with non-zero status.
- File search now skips dot directories.
- animanager now depends on ``mir.sqlite3m``.

Removed
^^^^^^^

- Removed ``fetch_titles`` command.  The rewritten titles caching
  logic does not need it.  (Due to a typo, the command wasn't
  available anyway.)

Fixed
^^^^^

- Fixed bug where ``enddate`` gets set to ``0`` instead of ``NULL``.

0.10.2 (2016-04-24)
-------------------

Added
^^^^^

- Added ``reset`` command.
- Added ``-c`` flag to ``unregister`` command.
- Added ``fetch_titles`` command.

Changed
^^^^^^^

- ``r`` alias changed from ``register`` command to ``reset`` command.
- ``search -a`` command now includes shows with any available
  unwatched episodes, not just the next unwatched episode.
- Rewrote command line code, so behavior will be different than before (e.g.,
  for help).

0.10.1 (2016-03-28)
-------------------

Added
^^^^^

- Debug logging.
- Add update command, which uses animedb results as opposed to anidb
  results for the add command.
- Friendlier presentation for AID parse errors.
- watching option added to search command.
- search command can now filter anime with available episodes to watch.

Changed
^^^^^^^

- Anime watching no longer includes broken symlinks.
- File picker now prefers files lower in alphabetical sorting (so v2
  is picked over v1, for example).
- Available episodes are displayed starting from the last watched
  episode, instead of displaying all available episodes.  Available
  episodes are also limited to the next eight, to account for anime
  with potentially hundreds of episodes.
- search command now orders by AID
- watch command only offers to bump if the next episode was watched.
- AnimeDB.search() changed to AnimeDB.select() with different
  semantics.
- Instead of caching AniDB anime data as local XML files, Animanager's
  own animedb now serves as a "cache".  The original workflow had a
  redundant step::

    anidb titles search -> fetch anidb anime data ->
    load anidb anime data into local animedb

  Now it is just::

    anidb titles search -> load anidb anime data into local animedb

Removed
^^^^^^^

- ashow command.
- fetch command.
- Script file support.  Automation will instead be supported via
  importing Animanager as a Python library.

0.10.0 (2016-03-26)
-------------------

Added
^^^^^

- Added command line interface.
- Added database migration and versioning.
- Added AniDB support.

Removed
^^^^^^^

- Removed everything, as this is a rewrite.
- Remove MyAnimeList support.
- Removed migration-tools.  Use 0.9.0 for migrations.

0.9.0 (2016-03-07)
------------------

This release is provided to "receive" migrated databases from 0.8.1.
This release is not feature complete or documented in any meaningful
sense, but enough features have been provided for basic life-support
management; type ``?`` after running ``animanager anime``.

0.8.1 (2016-03-07)
------------------

This release is provided solely to explain migration to 0.9.0.

0.8.0 (2016-01-23)
------------------

Added
^^^^^

- Added plan command.
- (gui command (GTK GUI for watching shows) was added, and then
  removed in 0457e2 because it is useless and cumbersome. Its
  existence is noted here for reference.)

Changed
^^^^^^^

- The database file path is now configured in the configuration file.
  It can still be overridden at the command line.
- Configuration loading now has defaults.
- Configuration loading now checks for missing values.
- watch command now searches in a configured directory instead of the
  current directory.
- watch command now searches for files recursively in designated directory.
- Registered series regular expressions now match anywhere in the
  filename, not just at the beginning.  The preceeding ``.*`` in the
  default pattern has been removed.

Fixed
^^^^^

- Fixed bug where episode regexp patterns matched case sensitive, and
  matched starting from the second character.
- Fixed exception catching in update command.

0.7.2 (2015-12-23)
------------------

Added
^^^^^

- Added ability to quit watch command.

0.7.1 (2015-10-05)
------------------

Changed
^^^^^^^

- Default status of added series is now "watching".
- Default regexp for registered series changed.  It should now match
  more intelligently.
- Ignore case when matching registered series.  This should now match
  more intelligently.
- Clean command now also removes series that are dropped.

Fixed
^^^^^

- Catch MAL querying error so the user doesn't see a stack trace.

0.7.0 (2015-10-04)
------------------

Added
^^^^^

- Added watching command.
- Added hold command.
- Added drop command.

Changed
^^^^^^^

- Instead of asking for confirmation when deleting files, files are
  now "trashed" into a subdirectory, where the user can recover them
  or purge them at his leisure.
- Watch command behavior changed, now prompts the user to select a
  file for each episode if there are multiple files, instead of
  attempting to choose one automatically by version and deleting the
  rest.

Removed
^^^^^^^

- Removed version detection in watch command.  Version matches in
  registered regular expressions are ignored.

Fixed
^^^^^

- Added missing triggers to schema to set complete when
  episode/chapter/volume is equal to the total.  Triggers need to be
  manually applied to existing databases.
