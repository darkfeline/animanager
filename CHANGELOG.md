# Change log

This projects uses [semantic versioning](http://semver.org/).

## 0.10.0 - 2016-03-26

### Added

- Added command line interface.
- Added database migration and versioning.
- Added AniDB support.

### Removed

- Removed everything, as this is a rewrite.
- Remove MyAnimeList support.
- Removed migration-tools.  Use 0.9.0 for migrations.

## 0.9.0 - 2016-03-07

This release is provided to "receive" migrated databases from 0.8.1.  This
release is not feature complete or documented in any meaningful sense, but enough
features have been provided for basic life-support management; type `?` after
running `animanager anime`.

## 0.8.1 - 2016-03-07

This release is provided solely to explain migration to 0.9.0.

## 0.8.0 - 2016-01-23

### Added

- Added plan command.
- (gui command (GTK GUI for watching shows) was added, and then removed in
  0457e2 because it is useless and cumbersome. Its existence is noted here for
  reference.)

### Changed

- The database file path is now configured in the configuration file.  It can
  still be overridden at the command line.
- Configuration loading now has defaults.
- Configuration loading now checks for missing values.
- watch command now searches in a configured directory instead of the current
  directory.
- watch command now searches for files recursively in designated directory.
- Registered series regular expressions now match anywhere in the filename, not
  just at the beginning.  The preceeding `.*` in the default pattern has been
  removed.

### Fixed

- Fixed bug where episode regexp patterns matched case sensitive, and matched
  starting from the second character.
- Fixed exception catching in update command.

## 0.7.2 - 2015-12-23

### Added

- Added ability to quit watch command.

## 0.7.1 - 2015-10-05

### Changed

- Default status of added series is now "watching".
- Default regexp for registered series changed.  It should now match more
  intelligently.
- Ignore case when matching registered series.  This should now match more
  intelligently.
- Clean command now also removes series that are dropped.

### Fixed

- Catch MAL querying error so the user doesn't see a stack trace.

## 0.7.0 - 2015-10-04

### Added

- Added watching command.
- Added hold command.
- Added drop command.

### Changed

- Instead of asking for confirmation when deleting files, files are now
  "trashed" into a subdirectory, where the user can recover them or purge them
  at his leisure.
- Watch command behavior changed, now prompts the user to select a file for each
  episode if there are multiple files, instead of attempting to choose one
  automatically by version and deleting the rest.

### Removed

- Removed version detection in watch command.  Version matches in registered
  regular expressions are ignored.

### Fixed

- Added missing triggers to schema to set complete when episode/chapter/volume
  is equal to the total.  Triggers need to be manually applied to existing
  databases.
