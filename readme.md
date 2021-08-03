[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/Version-0.8.0-blue.svg)](https://github.com/DCSBL/ha-homewizard-energy)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/Create%20release/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/Validation%20And%20Formatting/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/CodeQL/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
[![Downloads for latest release](https://img.shields.io/github/downloads/DCSBL/ha-homewizard-energy/latest/total.svg)](https://github.com/DCSBL/ha-homewizard-energy/releases/latest)

# HomeWizard Energy Integration
Custom integration for the [HomeWizard Energy Products](https://www.homewizard.nl/energie).

![HomeWizard Energy Logo](https://raw.githubusercontent.com/home-assistant/brands/master/custom_integrations/homewizard_energy/icon.png "HomeWizard Energy")

## Requirements
* This integration works with:
  * [HomeWizard wifi P1 mter](https://www.homewizard.nl/shop/homewizard-wi-fi-p1-meter)
  * [HomeWizard wifi kWh meter single phase](https://www.homewizard.nl/shop/homewizard-wi-fi-kwh-meter)
  * [HomeWizard wifi kWh meter 3-phase](https://www.homewizard.nl/shop/homewizard-wifi-3-fase-din-rail-kwh-meter)
* Make sure the HomeWizard Energy P1 Meter has been connected to the same network.
* Make sure you have mDNS/discovery enabled on your router.

## Installation
### HACS (https://hacs.xyz)
**This is the recommended method**
1. Install this integration from HACS (Search for 'HomeWizard Energy').
2. ❗ **Restart Home Assistant**.

### Manual installation
1. Download the zip `homewizard_energy.zip` from the [latest release](https://github.com/DCSBL/ha-homewizard-energy/releases/latest)
2. Extract this zip in `config/custom_components`. (The config folder where configuration.yaml can be found)
3. ❗**Restart Home Assistant**.
4. Please come back now and then to check if there is a new version available (this can be automated with HACS)

## Usage
1. Go to Configuration > Integrations.
2. Home Assistant should tell you that a new device has been 'discovered'. (if not, please read 'manual configuration')
3. Press configure to add this device, and give it a name if you want.
4. :tada:

### Manual configuration
If Home Assistant can't automaticly find your device, you can try to install your meter manually. 
1. Go to Configuration > Integrations > Add integration > search for 'HomeWizard Energy'.
2. Enter the IP address from your device (eg. `192.168.1.107`).

## Discussion
Please join us at [the HASS forum](https://community.home-assistant.io/t/wi-fi-p1-dsmr-dongle-homewizard-energy) or the Dutch website [Tweakers (NL)](https://gathering.tweakers.net/forum/list_messages/2002754/last)

## Frequent questions and issues
1. **Home Assistant tells my device is offline after updating this integration**
This is a known issue. Please restart your Home Assistant again. That should solve it for you.
2. **I get a 'connection refused' error when trying to connect to `http://<ip_address>/api/v1/data`**
Your P1 meter must be at firmware version '2.11' or higher. You can see this in the HomeWizard Energy app under 'Meters'. Your device should update within an hour after connecting it to the internet. If your device doesn't, contact HomeWizard Support.
3. **Is the HomeWizard Wi-Fi kWh meter supported?**
Yes, since 2021-06-03. YOu have to enable the API in the HomeWizard Energy app.
4. **Can I see the daily/weekly/montly usage and history with this integration?**
No. This integration is only for retreiving the data and making it available in Home Assistant. But you can create this feature yourself. [There](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441) [are](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/87) [some](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/114) [great](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/52) [examples](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/78).

## API documentation
[HomeWizard Energy local API](https://homewizard-energy-api.readthedocs.io/#)

## Disclaimer
This integration is not developed, nor supported by HomeWizard.
