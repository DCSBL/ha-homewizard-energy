
> ⚠️ **Make a back-up before installing this version. Your configuration will be migrated to Home Assistant Core.**

# HomeWizard Energy Integration
Custom integration for the [HomeWizard Energy Products](https://www.homewizard.nl/energie).

## Integration added to core :tada:
This integration is available in Core. This custom integration won't be maintained and eventually removed.  Click here to read more and install the core integration: https://home-assistant.io/integrations/homewizard/
<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=homewizard" class="my badge" target="_blank"><img src="https://my.home-assistant.io/badges/config_flow_start.svg"></a>

# Migration
**This integration is not maintained and will be removed**

From version [0.13.0](https://github.com/DCSBL/ha-homewizard-energy/releases), this custom integration only exists to allow migration of current configurations.
If you had a pre-0.13.0 version in use and you install this version, it will automaticly migrate to core.

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
        value_template: "{{ as_timestamp(states.sensor.p1_meter_<serial>_active_power.last_updated) }}"
```
Replace `p1_meter_<serial>_total_gas` to use the correct entity id. Now you can use `sensor. p1_meter_gas_timestamp`