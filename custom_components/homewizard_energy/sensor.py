"""Creates Homewizard Energy sensor entities."""

import logging
import async_timeout

from datetime import timedelta
from homeassistant import util
from homeassistant.const import (
    CONF_IP_ADDRESS,
    POWER_WATT,
    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
    PERCENTAGE,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import api, const

_LOGGER = logging.getLogger(__name__)

_PLATFORM = "sensor"

SENSORS = {
    const.ATTR_SMR_VERSION: {"icon": "mdi:gauge", "unit": POWER_WATT},
    const.ATTR_METER_MODEL: {"icon": "mdi:gauge", "unit": ""},
    const.ATTR_WIFI_SSID: {"icon": "mdi:gauge", "unit": ""},
    const.ATTR_WIFI_STRENGTH: {"icon": "mdi:gauge", "unit": PERCENTAGE},
    const.ATTR_TOTAL_POWER_IMPORT_T1_KWH: {
        "icon": "mdi:gauge",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_IMPORT_T2_KWH: {
        "icon": "mdi:gauge",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_EXPORT_T1_KWH: {
        "icon": "mdi:gauge",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_TOTAL_POWER_EXPORT_T2_KWH: {
        "icon": "mdi:gauge",
        "unit": ENERGY_KILO_WATT_HOUR,
    },
    const.ATTR_ACTIVE_POWER_W: {"icon": "mdi:gauge", "unit": POWER_WATT},
    const.ATTR_ACTIVE_POWER_L1_W: {"icon": "mdi:gauge", "unit": POWER_WATT},
    const.ATTR_ACTIVE_POWER_L2_W: {"icon": "mdi:gauge", "unit": POWER_WATT},
    const.ATTR_ACTIVE_POWER_L3_W: {"icon": "mdi:gauge", "unit": POWER_WATT},
    const.ATTR_TOTAL_GAS_M3: {"icon": "mdi:gauge", "unit": VOLUME_CUBIC_METERS},
    const.ATTR_GAS_TIMESTAMP: {"icon": "mdi:gauge", "unit": ""},
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""
    _LOGGER.info("Setting up sensor for HomeWizard Energy.")

    hw_api = api.HWEP1Api(entry.data[CONF_IP_ADDRESS])

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with async_timeout.timeout(10):
            return await hw_api.get_energy_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="p1 meter",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=5),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    # services.register_services(hass)
    async_add_entities(
        HWEP1MeterSensor(coordinator, entry.data[const.CONF_IP_ADDRESS], info_type)
        for info_type in SENSORS
    )

    return True


class HWEP1MeterSensor(CoordinatorEntity):
    """Representation of a HomeWizard Energy"""

    ip_address = None
    name = None

    def __init__(self, coordinator, ip_address, info_type):
        """Initializes the sensor."""

        super().__init__(coordinator)

        # Config attributes.
        self.name = f"P1 Meter - {info_type}"

        self.ip_address = ip_address
        self.info_type = info_type
        self.coordinator = coordinator

    @property
    def unique_id(self):
        """Return a unique id for the sensor."""
        unique_id = f"p1_meter_{self.ip_address}-{self.info_type}"
        return f"{util.slugify(unique_id)}"

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.info_type]["icon"]

    @property
    def state(self):
        """Returns state of meter."""
        return self.coordinator.data[self.info_type]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSORS[self.info_type]["unit"]