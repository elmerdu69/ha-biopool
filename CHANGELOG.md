# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

---

## 1.2.0 — 2026-10-10

### Added

- Reset-to-100% buttons for Active Oxygen, Bio-Bacter and UV lamp, attached to the corresponding devices.
- Reset values use the container capacities and UV lifetime configured in integration options.
- Local integration icons and logos for light and dark themes (Home Assistant 2026.3+).
- French and English configuration and options translations.

### Fixed

- Apply option changes immediately without discarding runtime energy counters.
- Load the button platform, use the correct force parameters and attach buttons to existing devices.
- Correct the translations directory and the missing ConfigEntry import.

### Changed

- Dynamic pump icons and updated UV icon.

### Validation and limitations

- The three consumable resets were tested successfully on a real installation running Home Assistant 2026.10.0.
- Python and JSON syntax validated; API commands and configurable reset values checked with simulated responses.
- Force buttons send force_uv, force_oxy and force_bacter. Their behavior in manual mode is still under validation.
- Reset buttons have no built-in confirmation dialog. Dashboard confirmations must be configured separately.

## [1.1.0] - 2026-08-19

### Added

- Added BioPool controller water temperature sensor (`water_temp`).
- Added optional external Home Assistant temperature source.
- Added forced temperature synchronization with the BioPool controller.
- Added automatic return to controller-estimated temperature when external temperature is disabled.
- Added temperature offset data (`temp_offset`).
- Added configurable Bio-Bacter container size.
- Added configurable Active Oxygen container size.
- Added configurable UV lamp lifetime.
- Added energy calculation from instantaneous power measurements.
- Added energy state restoration after Home Assistant restart.
- Added energy monitoring for equipment exposing a power sensor.

### Changed

- External temperature is synchronized only when its value changes.
- Forced temperature is sent to the BioPool controller with one decimal place.
- Pump runtime is displayed with one decimal place.
- Energy calculation is now handled consistently for supported equipment.
- Improved remaining lifetime and remaining quantity calculations.
- Improved sensor units, device classes and state classes.

### Fixed

- Fixed energy counter persistence across Home Assistant restarts.
- Fixed remaining value handling for UV, Bio-Bacter and Active Oxygen equipment.
- Fixed sensor units and measurement metadata.
- Fixed temperature forcing and removal of forced temperature.

---

[1.1.0]: https://github.com/elmerdu69/ha-biopool/releases/tag/v1.1.0

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
