# HomeWizard Energy P1 Meter
Custom integration for the [HomeWizard Energy P1 Meter](https://www.homewizard.nl/energie).

![HomeWizard Energy Logo](https://raw.githubusercontent.com/home-assistant/brands/master/custom_integrations/homewizard_energy/icon.png "HomeWizard Energy")

## Requirements
* Only the HomeWizard P1 Meter is supported at this moment.
* Your meter should run firmware 1.48 or higher. Check this in HomeWizard Energy app &#8594; Gear icon &#8594; Meters &#8594; (your meter) &#8594; Software. Contact [HomeWizard Support](https://energy.homewizard.net/nl/support/tickets/new) if this is not the case.
* Make sure the HomeWizard Energy P1 Meter has been connected to the same network as your Home Assistant installation and you know the IP address.

## Installation
### HACS (https://hacs.xyz)
> This is the recommended method
* Have HACS installed.
* Go to your HACS setup page.
* Press "Integrations" > 3 dots (upper-right) > 'Custom repositories'.
* Enter the URL of this repo (https://github.com/Unsigus/hass-homewizard-energy/), select 'Integration' category and press ADD.
* Restart Home Assistant.

### Manually
* Install the custom component by downloading it and copy it to the custom_components directory as usual.
* Restart Home Assistant.
* Devices will be found automatically.

## Usage
* Go to Configuration > Integrations > and add the 'HomeWizard Energy' integration.
* Enter the IP address of the P1 meter.
* Add the sensors you want to view in in your dashboard.

## Discussion
Please join us at [the HASS forum](https://community.home-assistant.io/t/wi-fi-p1-dsmr-dongle-homewizard-energy) or the Dutch website [Tweakers (NL)](https://gathering.tweakers.net/forum/list_messages/2002754/last)

## API documentation
[HomeWizard P1 Meter local API](https://energy.homewizard.net/en/support/solutions/articles/19000117051-homewizard-p1-meter-local-api-beta-)

## Todo's
Things still to do before it is ready for everyone

* ~Make repository HACS compatible~
* ~Make polling rate relevant to device~
* Prepare integration for other HomeWizard Energy devices
