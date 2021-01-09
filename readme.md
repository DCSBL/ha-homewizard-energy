<!--
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
-->
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/badge/Version-0.5.0-blue.svg)](https://github.com/d-sebel/ha-homewizard-energy)
[![Actions Status](https://github.com/d-sebel/ha-homewizard-energy/workflows/Create%20release/badge.svg)](https://github.com/d-sebel/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/d-sebel/ha-homewizard-energy/workflows/Validation%20And%20Formatting/badge.svg)](https://github.com/d-sebel/ha-homewizard-energy/actions)
[![Actions Status](https://github.com/d-sebel/ha-homewizard-energy/workflows/CodeQL/badge.svg)](https://github.com/d-sebel/ha-homewizard-energy/actions)

# HomeWizard Energy P1 Meter
Custom integration for the [HomeWizard Energy P1 Meter](https://www.homewizard.nl/energie).

![HomeWizard Energy Logo](https://raw.githubusercontent.com/home-assistant/brands/master/custom_integrations/homewizard_energy/icon.png "HomeWizard Energy")

## Requirements
* Only the HomeWizard P1 Meter is supported at this moment.
* Your meter should run firmware **2.11** or higher. Check this in HomeWizard Energy app &#8594; Gear icon &#8594; Meters &#8594; (your meter) &#8594; Software. Contact [HomeWizard Support](https://energy.homewizard.net/nl/support/tickets/new) if this is not the case.
* Make sure the HomeWizard Energy P1 Meter has been connected to the same network as your Home Assistant installation and you know the IP address.

## Installation
### HACS (https://hacs.xyz)
**This is the recommended method, release in [HACS defaults](https://github.com/hacs/default) pending**
<!--
* Install this integration from HACS (Search for 'HomeWizard Energy')
* Restart Home Assistant
-->
1. In HACS, go to Interations.
2. Click the 3 dots in the upper right.
3. Click 'Custom repositories'.
4. Add this repository (https://github.com/d-sebel/ha-homewizard-energy), select 'Integration' and click ADD.
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

## API documentation
[HomeWizard P1 Meter local API](https://energy.homewizard.net/en/support/solutions/articles/19000117051-homewizard-p1-meter-local-api-beta-)

## Disclaimer
This integration is not developed, nor supported by HomeWizard.
