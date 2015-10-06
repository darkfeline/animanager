# Changelog

## master

## v0.7.1

### Changed

- Default status of added series is now "watching".
- Default regexp for registered series changed.  It should now match more
  intelligently.
- Ignore case when matching registered series.  This should now match more
  intelligently.
- Clean command now also removes series that are dropped.

### Fixed

- Catch MAL querying error so the user doesn't see a stack trace.

## v0.7.0

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
