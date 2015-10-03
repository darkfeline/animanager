# Changelog

## master

### Added

- Added watching command.
- Added hold command.
- Added drop command.

### Changed

- Instead of asking for confirmation when deleting files, files are now
  "trashed" into a subdirectory, where the user can recover them or purge them
  at his leisure.

### Fixed

- Added missing triggers to schema to set complete when episode/chapter/volume
  is equal to the total.  Triggers need to be manually applied to existing
  databases.
