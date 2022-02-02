> ⚠️ This integration is available in Core. This custom integration won't be maintained and eventually removed.  Click here to install the core integration: https://home-assistant.io/integrations/homewizard/


# HomeWizard Energy Integration
Custom integration for the [HomeWizard Energy Products](https://www.homewizard.nl/energie).

## Use the official integration
**⚠️ Since [Home Assistant 2022.2](https://home-assistant.io/blog/2022/02/02/release-20222/) this integration is available in core! Click [here](https://home-assistant.io/integrations/homewizard/) for more info**

<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=homewizard" class="my badge" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg"></a>

I highly recommend to convert your configuration to use the core integration. This custom integration won't be updated from now on.

1. **Can I transfer my data to the core integration?**
No. I've spend a couple of hours to try this but it is not possible for now. I will keep an eye on this and will write a migrator when this is possible. You can keep using this custom component.
Give a thumps up or something to [this issue](https://github.com/DCSBL/ha-homewizard-energy/issues/74) so I can determine the priority.
2. **My devices are rediscovered**
This is the core integration that can't see that you already have the same device configured via this custom integration. You can ignore the discovered device.
3. **What if I have any problems with the integration?**
If the issues is with the core integration, you can open an issue [here](https://github.com/home-assistant/core/issues/new?assignees=&labels=&template=bug_report.yml). If you have an issue with the custom integration, you can open an issue [here](https://github.com/DCSBL/ha-homewizard-energy/issues)

## Still wan't to install the custom integration?
### Requirements
* This integration works with:
  * [HomeWizard wifi P1 meter](https://www.homewizard.nl/p1-meter)
  * [HomeWizard wifi kWh meter single phase](https://www.homewizard.nl/kwh-meter)
  * [HomeWizard wifi kWh meter 3-phase](https://www.homewizard.nl/kwh-meter)
  * [HomeWizard wifi Energy Socket](https://www.homewizard.nl/energy-socket)
* Make sure the HomeWizard Energy device has been connected to the same network.

### Installation
#### HACS (https://hacs.xyz)
1. Install this integration from HACS (Search for 'HomeWizard Energy').
2. ❗ **Restart Home Assistant**.

#### Manual installation
1. Download the zip `homewizard_energy.zip` from the [latest release](https://github.com/DCSBL/ha-homewizard-energy/releases/latest)
2. Extract this zip in `config/custom_components`. (The config folder where configuration.yaml can be found)
3. ❗**Restart Home Assistant**.
4. Please come back now and then to check if there is a new version available (this can be automated with HACS)

### Usage
1. Go to Configuration > Integrations.
2. Home Assistant should tell you that a new device has been 'discovered'. (if not, please read 'manual configuration')
3. Press configure to add this device, and give it a name if you want.
4. :tada:

#### Manual configuration
If Home Assistant can't automaticly find your device, you can try to install your meter manually. 
1. Go to Configuration > Integrations > Add integration > search for 'HomeWizard Energy'.
2. Enter the IP address from your device (eg. `192.168.1.107`).

### Discussion
Please join us at [the HASS forum](https://community.home-assistant.io/t/wi-fi-p1-dsmr-dongle-homewizard-energy) or the Dutch website [Tweakers (NL)](https://gathering.tweakers.net/forum/list_messages/2002754/last)

### Frequent questions and issues
1. **Home Assistant tells my device is offline after updating this integration**
This is a known issue. Please restart your Home Assistant again. That should solve it for you.
2. **I get a 'connection refused' error when trying to connect to `http://<ip_address>/api/v1/data`**
Your P1 meter must be at firmware version `2.11` or higher. You can see this in the HomeWizard Energy app under 'Meters'. Your device should update within an hour after connecting it to the internet. If your device doesn't, contact HomeWizard Support.
3. **Is the HomeWizard Wi-Fi kWh meter supported?**
Yes, since 2021-06-03. You have to enable the API in the HomeWizard Energy app.
4. **Can I see the daily/weekly/montly usage and history with this integration?**
Yes, add the device to the [Home Energy Management](https://www.home-assistant.io/docs/energy/) dashboard

### API documentation
[HomeWizard Energy local API](https://homewizard-energy-api.readthedocs.io/#)

### Disclaimer
This integration is not developed, nor supported by HomeWizard.
