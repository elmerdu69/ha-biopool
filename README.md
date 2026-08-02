<p align="center">
  <img src="images/banner.png" alt="BioPool for Home Assistant">
</p>

<h1 align="center">
BioPool Connect Integration for Home Assistant
</h1>

<p align="center">
Monitor and control your BioPool installation directly from Home Assistant.
</p>

<p align="center">

  ![GitHub release](https://img.shields.io/github/v/release/elmerdu69/ha-biopool)
  ![GitHub Downloads](https://img.shields.io/github/downloads/elmerdu69/ha-biopool/total)
  ![GitHub stars](https://img.shields.io/github/stars/elmerdu69/ha-biopool)
  ![GitHub License](https://img.shields.io/github/license/elmerdu69/ha-biopool)

</p>

---

## Features

* 🏊 Pool operating mode selection
* 🔄 Filtration pump control
* 💡 UV lamp control
* 🧪 Bio-Bacter injection control
* 🫧 Active Oxygen injection control
* ⚡ Real-time power consumption
* 🔋 Energy monitoring
* ⏱ Pump runtime monitoring
* 💧 Remaining Bio-Bacter level
* 💧 Remaining Active Oxygen level
* 💡 Remaining UV lamp lifetime

The integration automatically creates devices and entities that integrate seamlessly with the Home Assistant device registry.

---

## Supported equipment

The integration automatically discovers and creates the following devices:

### Pool Controller

* Operating mode selector

### Filtration Pump

* On/Off switch
* Running status
* Instant power (W)
* Energy consumption (kWh)
* Total operating time (h)

### UV Lamp

* On/Off switch
* Running status
* Instant power (W)
* Energy consumption (kWh)
* Remaining lamp lifetime (%)

### Bio-Bacter

* On/Off switch
* Running status
* Remaining product (%)

### Active Oxygen

* On/Off switch
* Running status
* Remaining product (%)

---

## Installation

### Manual installation

1. Copy the `biopool` folder into:

```text
config/custom_components/
```

2. Restart Home Assistant.

3. Go to:

**Settings → Devices & Services → Add Integration**

4. Search for:

```
BioPool
```

5. Enter your BioPool credentials.

The integration will automatically discover your pool controller.

---

## Configuration

Only your BioPool account credentials are required.

* Username
* Password

No additional configuration is necessary.

---

## Entities

The integration creates:

| Device          | Entities                                                 |
| --------------- | -------------------------------------------------------- |
| Pool            | Operating mode                                           |
| Filtration Pump | Switch, Binary Sensor, Power, Energy, Runtime            |
| UV Lamp         | Switch, Binary Sensor, Power, Energy, Remaining lifetime |
| Bio-Bacter      | Switch, Binary Sensor, Remaining quantity                |
| Active Oxygen   | Switch, Binary Sensor, Remaining quantity                |

---

## Screenshots

### Devices

The integration automatically creates five Home Assistant devices.

<p align="center">
  <img src="images/devices.png" width="700">
</p>


### Dashboard

Example Lovelace dashboard.

<p align="center">
  <img src="images/dashboard.png" width="700">
</p>


### Energy Dashboard

The filtration pump and UV lamp expose energy sensors compatible with the Home Assistant Energy Dashboard.

<p align="center">
  <img src="images/energy.png" width="700">
</p>

---

## Compatibility

Tested with:

* Home Assistant 2026.x
* BioPool Connect Cloud

---

## Roadmap

### Version 1.1

* HACS support
* Diagnostics
* Better translations
* Additional sensors

### Version 1.2

* Services
* Advanced diagnostics
* Additional pool statistics

---

## Issues

If you encounter a problem, please open an issue on GitHub and include:

* Home Assistant version
* Integration version
* Relevant logs

---

## License

This project is licensed under the MIT License.
