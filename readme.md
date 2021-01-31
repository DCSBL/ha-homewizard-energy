[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/Version-0.4.2-blue.svg)](https://github.com/DCSBL/ha-homewizard-energy)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/Create%20release/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/Validation%20And%20Formatting/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/DCSBL/ha-homewizard-energy/workflows/CodeQL/badge.svg)](https://github.com/DCSBL/ha-homewizard-energy/actions)
<!--[![Downloads for latest release](https://img.shields.io/github/downloads/DCSBL/ha-homewizard-energy/latest/total.svg)](https://github.com/DCSBL/ha-homewizard-energy/releases/latest)-->

> :exclamation: You most likely see this integration due to a bug in HACS. This will hopefully be fixed soon. See [hacs#1797](https://github.com/hacs/integration/issues/1797).

# HomeWizard Energy P1 Meter
Custom integration for the [HomeWizard Energy P1 Meter](https://www.homewizard.nl/energie).

![HomeWizard Energy Logo](https://raw.githubusercontent.com/home-assistant/brands/master/custom_integrations/homewizard_energy/icon.png "HomeWizard Energy")

## Requirements
* Only the HomeWizard P1 Meter is supported at this moment.
* Your meter should run firmware '2.11' or higher. Check this in HomeWizard Energy app &#8594; Gear icon &#8594; Meters &#8594; (your meter) &#8594; Software. Contact [HomeWizard Support](https://energy.homewizard.net/nl/support/tickets/new) if this is not the case.
* Make sure the HomeWizard Energy P1 Meter has been connected to the same network as your Home Assistant installation and you know the IP address.

## Installation
### HACS (https://hacs.xyz)
**This is the recommended method, release in [HACS defaults](https://github.com/hacs/default) pending**
<!--
* Install this integration from HACS (Search for 'HomeWizard Energy')
* Restart Home Assistant
-->
1. In HACS, go to 'integrations'.
2. Click the 3 dots in the upper right.
3. Click 'Custom repositories'.
4. Add this repository (https://github.com/DCSBL/ha-homewizard-energy), select 'Integration' and click ADD.
5. Click 'Install' in the 'New repository' card, and install it.
6. **Restart Home Assistant**.

### Manually
1. Install the custom component by downloading it and copy it to the custom_components directory as usual.
2. Restart Home Assistant.

## Usage
1. Go to Configuration > Integrations > and add the 'HomeWizard Energy' integration.
2. Enter the IP address of the P1 meter.
3. Add the sensors you want to view in in your dashboard.

## Discussion
Please join us at [the HASS forum](https://community.home-assistant.io/t/wi-fi-p1-dsmr-dongle-homewizard-energy) or the Dutch website [Tweakers (NL)](https://gathering.tweakers.net/forum/list_messages/2002754/last)

## Frequent questions and issues
1. **I get a 'connection refused' error when trying to connect to `http://<ip_address>/api/v1/data`**
Your device is not at firmware version '2.11' or higher. You can see this in the HomeWizard Energy app under 'Meters'. Your device should update within an hour after connecting it to the internet. If your device doesn't, contact HomeWizard Support.
2. **I have entered an IP address in the setup, but there is no data**
See #1
3. **I can't see the intergration from `Configuration > Integrations`**
Restart your HA installation. This loads the integration. If you still have issues, you can try installing 0.5.0 (currently in beta). This version has a new way of loading the integration.
4. **Is the HomeWizard Wi-Fi kWh meter supported?**
When the API is released for the kWh meter, this integration will support it.
5. **Can I see the daily/weekly/montly usage and history with this integration?**
No. This integration is only for retreiving the data and making it available in Home Assistant. But you can create this feature yourself. [There](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441) [are](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/87) [some](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/114) [great](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/52) [examples](https://community.home-assistant.io/t/custom-component-homewizard-energy-wifi-p1-meter/227441/78).

## API documentation
[HomeWizard P1 Meter local API](https://energy.homewizard.net/en/support/solutions/articles/19000117051-homewizard-p1-meter-local-api-beta-)

## Disclaimer
This integration is not developed, nor supported by HomeWizard.
