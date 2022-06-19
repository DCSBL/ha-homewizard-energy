
# HomeWizard Energy Integration (Archived)
The old custom integration for the [HomeWizard Energy Products](https://www.homewizard.nl/energie). This repo is archived for references and if you want to run the migration.

## Integration added to core :tada:
This integration is available in Core. This custom integration won't be maintained and eventually removed.  Click here to read more and install the core integration: https://home-assistant.io/integrations/homewizard/

<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=homewizard" class="my badge" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg"></a>

# Migration
This custom integration only exists to allow migration of current configurations. If you had a `pre-0.13.0` version in use and you install this version, it will automaticly migrate to core. **Make sure to have Home Assistant 2022.2.2 or later installed.**

## FAQ
1. **What if I have any problems with the integration?**
If the issues is with the core integration, you can open an issue [here](https://github.com/home-assistant/core/issues/new?assignees=&labels=&template=bug_report.yml). If you have an issue with the custom integration, you can open an issue [here](https://github.com/DCSBL/ha-homewizard-energy/issues)
2. **Where is `gas_timestamp` and `meter_model`?**
Meter model is renamed to `Smart Meter Model`. Gas timestamp is removed because it is the same as 'last updated total gas'. You can get it back with a template sensor:
```
# configuration.yaml
sensor:
  - platform: template
    sensors:
      p1_meter_gas_timestamp:
        friendly_name: "Gas Timestamp"
        device_class: timestamp
        value_template: "{{ states.sensor.p1_meter_<serial>_total_gas.last_updated }}"
```
Replace `p1_meter_<serial>_total_gas` to use the correct entity id. Now you can use `sensor.p1_meter_gas_timestamp`
