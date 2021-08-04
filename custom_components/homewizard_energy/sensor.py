"""Creates Homewizard Energy sensor entities."""
import asyncio
import logging
from typing import Any, Final

import aiohwenergy
import async_timeout
from homeassistant.components.sensor import (
    ATTR_LAST_RESET,
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import (
    CONF_ID,
    CONF_STATE,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TIMESTAMP,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    POWER_WATT,
    VOLUME_CUBIC_METERS,
)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util.dt import utc_from_timestamp

from .const import (
    ATTR_ACTIVE_POWER_L1_W,
    ATTR_ACTIVE_POWER_L2_W,
    ATTR_ACTIVE_POWER_L3_W,
    ATTR_ACTIVE_POWER_W,
    ATTR_GAS_TIMESTAMP,
    ATTR_METER_MODEL,
    ATTR_SMR_VERSION,
    ATTR_TOTAL_GAS_M3,
    ATTR_TOTAL_POWER_EXPORT_T1_KWH,
    ATTR_TOTAL_POWER_EXPORT_T2_KWH,
    ATTR_TOTAL_POWER_IMPORT_T1_KWH,
    ATTR_TOTAL_POWER_IMPORT_T2_KWH,
    ATTR_WIFI_SSID,
    ATTR_WIFI_STRENGTH,
    CONF_API,
    CONF_DATA,
    CONF_MODEL,
    CONF_OVERRIDE_POLL_INTERVAL,
    CONF_POLL_INTERVAL_SECONDS,
    CONF_SW_VERSION,
    COORDINATOR,
    DEFAULT_OVERRIDE_POLL_INTERVAL,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DOMAIN,
)

Logger = logging.getLogger(__name__)

SENSORS: Final[list[SensorEntityDescription]] = [
    SensorEntityDescription(
        key=ATTR_SMR_VERSION,
        name="SMR version",
        icon="mdi:wifi",
    ),
    SensorEntityDescription(
        key=ATTR_METER_MODEL,
        name="Model",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key=ATTR_WIFI_SSID,
        name="Wifi SSID",
        icon="mdi:wifi",
        unit_of_measurement="",
    ),
    SensorEntityDescription(
        key=ATTR_WIFI_STRENGTH,
        name="Wifi Strength",
        icon="mdi:wifi",
        unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_TOTAL_POWER_IMPORT_T1_KWH,
        name="Total power import T1",
        icon="mdi:home-import-outline",
        unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_TOTAL_POWER_IMPORT_T2_KWH,
        name="Total power import T2",
        icon="mdi:home-import-outline",
        unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_TOTAL_POWER_EXPORT_T1_KWH,
        name="Total power export T1",
        icon="mdi:home-export-outline",
        unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_TOTAL_POWER_EXPORT_T2_KWH,
        name="Total power export T2",
        icon="mdi:home-export-outline",
        unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_ACTIVE_POWER_W,
        name="Active power",
        icon="mdi:transmission-tower",
        unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_ACTIVE_POWER_L1_W,
        name="Active power L1",
        icon="mdi:transmission-tower",
        unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_ACTIVE_POWER_L2_W,
        name="Active power L2",
        icon="mdi:transmission-tower",
        unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_ACTIVE_POWER_L3_W,
        name="Active power L3",
        icon="mdi:transmission-tower",
        unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_TOTAL_GAS_M3,
        name="Total gas",
        icon="mdi:fire",
        unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_GAS_TIMESTAMP,
        name="Gas timestamp",
        icon="mdi:timeline-clock",
        device_class=DEVICE_CLASS_TIMESTAMP,
    ),
]


def get_update_interval(entry, energy_api):

    if entry.options.get(CONF_OVERRIDE_POLL_INTERVAL, DEFAULT_OVERRIDE_POLL_INTERVAL):
        return entry.options.get(
            CONF_POLL_INTERVAL_SECONDS, DEFAULT_POLL_INTERVAL_SECONDS
        )

    try:
        product_type = energy_api.device.product_type
    except AttributeError:
        product_type = "Unknown"

    if product_type == "HWE-P1":
        try:
            smr_version = energy_api.data.smr_version
            if smr_version == 50:
                return 1
            else:
                return 5
        except AttributeError:
            pass

    elif product_type == "SDM230-wifi" or product_type == "SDM630-wifi":
        return 1

    return 10


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""
    Logger.info("Setting up sensor for HomeWizard Energy.")

    energy_api = hass.data[DOMAIN][entry.data["unique_id"]][CONF_API]

    # Validate connection
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

    coordinator = hass.data[DOMAIN][entry.data["unique_id"]][COORDINATOR]

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    if energy_api.data != None:
        entities = []
        for description in SENSORS:
            if description.key in energy_api.data.available_datapoints:
                entities.append(HWEnergySensor(coordinator, entry.data, description))
        async_add_entities(entities, update_before_add=True)

        return True
    else:
        await energy_api.close()
        return False


class HWEnergySensor(CoordinatorEntity, SensorEntity):
    """Representation of a HomeWizard Energy"""

    host = None
    name = None
    entry_data = None
    unique_id = None

    def __init__(self, coordinator, entry_data, description):
        """Initializes the sensor."""

        super().__init__(coordinator)
        self.entity_description = description
        self.coordinator = coordinator
        self.entry_data = entry_data

        # Config attributes.
        self.name = "%s %s" % (entry_data["custom_name"], description.name)
        self.host = entry_data["host"]
        self.data_type = description.key
        self.unique_id = "%s_%s" % (entry_data["unique_id"], description.key)
        self._attr_last_reset = utc_from_timestamp(0)

    @property
    def device_info(self) -> DeviceInfo:
        return {
            "name": self.entry_data["custom_name"],
            "manufacturer": "HomeWizard",
            "sw_version": self.data[CONF_SW_VERSION],
            "model": self.data[CONF_MODEL],
            "identifiers": {(DOMAIN, self.data[CONF_ID])},
        }

    @property
    def data(self) -> dict[str:Any]:
        """Return data from DataUpdateCoordinator"""
        return self.coordinator.data

    @property
    def icon(self):
        """Return the icon."""
        return self.entity_description.icon

    @property
    def state(self):
        """Returns state of meter."""
        return self.data[CONF_DATA][self.data_type]

    @property
    def available(self):
        """Returns state of meter."""
        return self.data_type in self.data[CONF_DATA]


async def async_get_aiohwenergy_from_entry_data(entry_data):
    """Create a HomewizardEnergy object from entry data."""

    Logger.debug(
        "%s async_get_aiohwenergy_from_entry_data\nentry_data:\n%s"
        % (__name__, str(entry_data))
    )

    return aiohwenergy.HomeWizardEnergy(entry_data["host"])
