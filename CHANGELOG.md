# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-08-02

### 🎉 Initial Release

First public release of the BioPool Connect integration for Home Assistant.

### Added

* Initial Home Assistant integration for BioPool Connect
* Configuration Flow support
* Automatic device discovery
* Automatic creation of Home Assistant devices
* Pool operating mode selector
* Filtration pump control
* UV lamp control
* Bio-Bacter control
* Active Oxygen control
* Pump running status
* UV lamp running status
* Bio-Bacter running status
* Active Oxygen running status
* Pump power sensor
* Pump energy sensor
* Pump operating time sensor
* UV lamp power sensor
* UV lamp energy sensor
* UV lamp remaining lifetime sensor
* Bio-Bacter remaining quantity sensor
* Active Oxygen remaining quantity sensor

### Improved

* Reworked entity architecture
* One Home Assistant device per physical BioPool equipment
* Unified device registry support
* Optimized update coordinator
* Immediate state refresh after switch commands
* Cleaner internal API structure
* Improved entity naming
* Improved unique IDs
* Better code organization

### Fixed

* Correct calculation of remaining Bio-Bacter percentage
* Correct calculation of remaining Active Oxygen percentage
* Correct calculation of remaining UV lamp lifetime
* Correct pump runtime reporting
* Fixed switch state synchronization after commands
* Fixed multiple entity initialization issues
* Fixed coordinator refresh issues
* Fixed device registration issues

---

[1.0.0]: https://github.com/elmerdu69/ha-biopool/releases/tag/v1.0.0
