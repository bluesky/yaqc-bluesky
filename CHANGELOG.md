# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed
- state of busy no longer returned when devices are read
- happi name field no longer overloaded, upstream now allows short names
- happi now pinned to >= 1.9.0

### Added
- clients to has-position daemons now implement @property position, a common convention in bluesky

### Removed
- no longer implement "set" for hardware without position (had raised NotImplementedError)

## [2021.1.1]

### Changed
- overloaded happi default for item name requirements: now any valid python identifier works

## [2021.1.0]

### Added
- happi support
- happi is now a dependency

### Changed
- removed base attribute stop (None) that only existed to pass bluesky ducktype checks
- added bluesky as explicit dependency, pinned to newer than 1.6.6

## [2020.07.1]

### Fixed
- fixed broken distribution from duplicate key in pyproject.toml

## [2020.07.0]

### Added
- initial release

[Unreleased]: https://github.com/bluesky/yaqc-bluesky/compare/v2021.1.1...HEAD
[2021.1.1]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.1.0...v2021.1.1
[2021.1.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.07.1...v2021.1.0
[2020.07.1]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://github.com/bluesky/yaqc-bluesky/releases/tag/v2020.07.0
