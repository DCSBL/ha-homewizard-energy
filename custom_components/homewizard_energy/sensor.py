"""Creates Homewizard Energy sensor entities."""
import asyncio
import logging
import sys
from datetime import timedelta

import aiohwenergy
import async_timeout
from homeassistant.const import (
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    POWER_WATT,
    VOLUME_CUBIC_METERS,
)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import const

Logger = logging.getLogger(__name__)

_PLATFORM = "sensor"

SENSORS = {
    const.ATTR_SMR_VERSION: {"name": "SMR version", "icon": "mdi:pound", "unit": ""},
    const.ATTR_METER_MODEL: {"name": "Model", "icon": "mdi:counter", "unit": ""},
    const.ATTR_WIFI_SSID: {"name": "Wifi SSID", "icon": "mdi:wifi", "unit": ""},
    const.ATTR_WIFI_STRENGTH: {
        "name": "Wifi Strength",
        "icon": "mdi:wifi",
        "unit": PERCENTAGE,
    },
    const.ATTR_TOTAL_POWER_IMPORT_T1_KWH: {
        "name": "Total power import T1",
        "icon": "mdi:home-import-outline",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_IMPORT_T2_KWH: {
        "name": "Total power import T2",
        "icon": "mdi:home-import-outline",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_EXPORT_T1_KWH: {
        "name": "Total power export T1",
        "icon": "mdi:home-export-outline",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_EXPORT_T2_KWH: {
        "name": "Total power export T2",
        "icon": "mdi:home-export-outline",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_ACTIVE_POWER_W: {
        "name": "Active power",
        "icon": "mdi:transmission-tower",
        "unit": POWER_WATT,
    },
    const.ATTR_ACTIVE_POWER_L1_W: {
        "name": "Active power L1",
        "icon": "mdi:transmission-tower",
        "unit": POWER_WATT,
    },
    const.ATTR_ACTIVE_POWER_L2_W: {
        "name": "Active power L2",
        "icon": "mdi:transmission-tower",
        "unit": POWER_WATT,
    },
    const.ATTR_ACTIVE_POWER_L3_W: {
        "name": "Active power L3",
        "icon": "mdi:transmission-tower",
        "unit": POWER_WATT,
    },
    const.ATTR_TOTAL_GAS_M3: {
        "name": "Total gas",
        "icon": "mdi:fire",
        "unit": VOLUME_CUBIC_METERS,
    },
    const.ATTR_GAS_TIMESTAMP: {
        "name": "Gas timestamp",
        "icon": "mdi:timeline-clock",
        "unit": "",
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""
    Logger.info("Setting up sensor for HomeWizard Energy.")

    energy_api = hass.data[const.DOMAIN][entry.data["unique_id"]]

    initialized = False
    try:
        with async_timeout.timeout(10):
            await energy_api.initialize()
            initialized = True

    except (asyncio.TimeoutError, aiohwenergy.RequestError):
        Logger.error(
            "Error connecting to the Energy device at %s",
            energy_api._host,
        )
        raise ConfigEntryNotReady

    except aiohwenergy.AioHwEnergyException:
        Logger.exception("Unknown Energy API error occurred")
        raise ConfigEntryNotReady

    except Exception:  # pylint: disable=broad-except
        Logger.exception(
            "Unknown error connecting with Energy Device at %s",
            energy_api._host["host"],
        )
        return False

    finally:
        if not initialized:
            await energy_api.close()

    async def async_update_data():
        """Fetch data from API endpoint."""
        data = {}
        async with async_timeout.timeout(10):
            try:
                status = await energy_api.data.update()

                if status:
                    for datapoint in energy_api.data.available_datapoints:
                        data[datapoint] = getattr(energy_api.data, datapoint)

                return data
            except AttributeError:
                Logger.error("Datapoint missing")
                return
            except aiohwenergy.errors.InvalidState:
                Logger.error("Failed tot fetch new data")
            finally:
                return data

    # Determine update interval
    ## Default update interval
    update_interval = 5

    try:
        product_type = energy_api.device.product_type
    except AttributeError:
        product_type = "Unknown"

    if product_type == "HWE-P1":
        try:
            smr_version = energy_api.data.smr_version
            if smr_version == 50:
                update_interval = 1
            else:
                update_interval = 5
        except AttributeError:
            pass

    if product_type == "SDM230-wifi" or product_type == "SDM630-wifi":
        update_interval = 1

    coordinator = DataUpdateCoordinator(
        hass,
        Logger,
        # Name of the data. For logging purposes.
        name=entry.data["name"],
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=update_interval),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    if energy_api.data != None:
        entities = []
        for datapoint in energy_api.data.available_datapoints:
            entities.append(device_hwe(coordinator, entry.data, datapoint))
        async_add_entities(entities, update_before_add=True)

        return True
    else:
        await energy_api.close()
        return False


class device_hwe(CoordinatorEntity):
    """Representation of a HomeWizard Energy"""

    host = None
    name = None
    unique_id = None
    entry_data = None

    def __init__(self, coordinator, entry_data, info_type):
        """Initializes the sensor."""

        super().__init__(coordinator)

        # Config attributes.
        self.name = "%s %s" % (entry_data["custom_name"], SENSORS[info_type]["name"])

        self.host = entry_data["host"]
        self.info_type = info_type
        self.coordinator = coordinator
        self.entry_data = entry_data
        self.unique_id = "%s_%s" % (entry_data["unique_id"], info_type)

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.info_type]["icon"]

    @property
    def state(self):
        """Returns state of meter."""
        return self.coordinator.data[self.info_type]

    @property
    def available(self):
        """Returns state of meter."""
        return self.info_type in self.coordinator.data

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSORS[self.info_type]["unit"]


async def async_get_aiohwenergy_from_entry_data(entry_data):
    """Create a HomewizardEnergy object from entry data."""

    Logger.debug(
        "%s async_get_aiohwenergy_from_entry_data\nentry_data:\n%s"
        % (__name__, str(entry_data))
    )

    return aiohwenergy.HomeWizardEnergy(entry_data["host"])
