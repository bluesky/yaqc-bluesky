# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2023.8.0]

### Added
- daemons supporting is-discrete now can be set according to their identifiers

### Changed
- properties now appear as sub-devices

### Fixed
- sensors no-longer force a measure at connect-time (this requires sensors to actually be traits compliant)

## [2022.4.1]

### Fixed
- More error tolerant wait until still method which properly sets the exception of the status object

## [2022.4.0]

### Fixed
- namespace dependent hardware to avoid name collisions
- Invalid splatting of has mapping values into an append call, which only takes one argument

### Added
- "independent" flag to mapping added fields marking them as independent variables that should not be treated as "channels"

## [2022.1.0]

### Added
- human readable repr for device
- Handling of devices which provide dependent hardware

## [2021.12.0]

### Changed
- Use yaq properties to fill out read/configuration
- No longer use `{name}_readback` and `{name}_setpoint` (replaced by `{name}` and `{name}_destination`)

## [2021.9.0]

### Changed
- state of busy no longer returned when devices are read
- happi name field no longer overloaded, upstream now allows short names
- happi now pinned to >= 1.9.0
- Default for units and shape if not provided for the daemon
- Sensor shapes properly applied in describe
- Use "array" dtype for sensor channels with a shape

### Added
- clients to has-position daemons now implement @property position, a common convention in bluesky
- handling of has-mapping trait to provide correlated dimensions between mapping and arrays

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

[Unreleased]: https://github.com/bluesky/yaqc-bluesky/compare/v2023.8.0...master
[2023.8.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2022.4.1...v2023.8.0
[2022.4.1]: https://github.com/bluesky/yaqc-bluesky/compare/v2022.4.0...v2022.4.1
[2022.4.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2022.1.0...v2022.4.0
[2022.1.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2021.12.0...v2022.1.0
[2021.12.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2021.9.0...v2021.12.0
[2021.9.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.1.1...v2021.9.0
[2021.1.1]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.1.0...v2021.1.1
[2021.1.0]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.07.1...v2021.1.0
[2020.07.1]: https://github.com/bluesky/yaqc-bluesky/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://github.com/bluesky/yaqc-bluesky/releases/tag/v2020.07.0
