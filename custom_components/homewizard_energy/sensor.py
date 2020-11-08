"""Creates Homewizard Energy sensor entities."""

import logging

import requests
from homeassistant import util
from homeassistant.helpers import config_validation, entity_platform
from homeassistant.helpers.entity import Entity

from . import api, const, services

_LOGGER = logging.getLogger(__name__)

_PLATFORM = "sensor"

SENSORS = {
    const.ATTR_SMR_VERSION: "mdi:gauge",
    const.ATTR_METER_MODEL: "mdi:gauge",
    const.ATTR_WIFI_SSID: "mdi:gauge",
    const.ATTR_WIFI_STRENGTH: "mdi:gauge",
    const.ATTR_TOTAL_POWER_IMPORT_T1_KWH: "mdi:gauge",
    const.ATTR_TOTAL_POWER_IMPORT_T2_KWH: "mdi:gauge",
    const.ATTR_TOTAL_POWER_EXPORT_T1_KWH: "mdi:gauge",
    const.ATTR_TOTAL_POWER_EXPORT_T2_KWH: "mdi:gauge",
    const.ATTR_ACTIVE_POWER_W: "mdi:gauge",
    const.ATTR_ACTIVE_POWER_L1_W: "mdi:gauge",
    const.ATTR_ACTIVE_POWER_L2_W: "mdi:gauge",
    const.ATTR_ACTIVE_POWER_L3_W: "mdi:gauge",
    const.ATTR_TOTAL_GAS_M3: "mdi:gauge",
    const.ATTR_GAS_TIMESTAMP: "mdi:gauge",
}


async def async_setup_entry(hass, config, async_add_entities):
    """Adds HomeWizard Energy to the list of senros."""
    _LOGGER.info("Setting up sensor for HomeWizard Energy.")

    # services.register_services(hass)
    async_add_entities(
        HWEP1MeterSensor(hass, config.data[const.CONF_IP_ADDRESS], info_type)
        for info_type in SENSORS
    )


class HWEP1MeterSensor(Entity):
    """Representation of a HomeWizard Energy"""

    hass = None
    ip_address = None
    name = None

    def __init__(self, hass, ip_address, info_type):
        """Initializes the sensor."""
        _LOGGER.info(f"Started Homewizard Energy with IP {ip_address}")

        _LOGGER.info(f"{info_type}")

        # Config attributes.
        self.name = f"P1 Meter - {info_type}"

        self.hass = hass
        self.ip_address = ip_address
        self.info_type = info_type

        # Internal attributes.
        # self.smr_version = None
        # self.meter_model = None
        # self.wifi_ssid = None
        # self.wifi_strength = None
        # self.total_power_import_t1_kwh = None
        # self.total_power_import_t2_kwh = None
        # self.total_power_export_t1_kwh = None
        # self.total_power_export_t2_kwh = None
        # self.active_power_w = None
        # self.active_power_l1_w = None
        # self.active_power_l2_w = None
        # self.active_power_l3_w = None
        # self.total_gas_m3 = None
        # self.gas_timestamp = None

        # self._api = api.HWEP1Api(self._ip_address)

        _LOGGER.debug(f"Set up completed.")

    # Properties.
    # @property
    # def entity_id(self):
    #     """Returns the entity ID for this remote."""
    #     return f"{_PLATFORM}.{self.entity_id}"

    # @property
    # def name(self):
    #     """Returns the display name of this meter."""
    #     return self._name or self._device_name

    @property
    def unique_id(self):
        """Return a unique id for the sensor."""
        unique_id = f"p1_meter_{self.ip_address}-{self.info_type}"
        _LOGGER.debug(f"Unique ID = {unique_id}.")
        return f"{util.slugify(unique_id)}"

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.info_type]

    @property
    def state(self):
        """Returns state of meter."""
        return 0
        # self.active_power_w

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "w"

    # Attributes.
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "version": "ok"
            # "smr_version": self.smr_version,
            # "meter_model": self.meter_model,
            # "wifi_ssid": self.wifi_ssid,
            # "wifi_strength": self.wifi_strength,
            # "total_power_import_t1_kwh": self.total_power_import_t1_kwh,
            # "total_power_import_t2_kwh": self.total_power_import_t2_kwh,
            # "total_power_export_t1_kwh": self.total_power_export_t1_kwh,
            # "total_power_export_t2_kwh": self.total_power_export_t2_kwh,
            # "active_power_w": self.active_power_w,
            # "active_power_l1_w": self.active_power_l1_w,
            # "active_power_l2_w": self.active_power_l2_w,
            # "active_power_l3_w": self.active_power_l3_w,
            # "total_gas_m3": self.total_gas_m3,
            # "gas_timestamp": self.gas_timestamp,
        }

    # Services.

    def update(self):
        """Updates device status."""

        # info = self._api.get_energy_data()

        # self.smr_version = info.get(const.ATTR_SMR_VERSION, {})
        # self.meter_model = info.get(const.ATTR_METER_MODEL, {})
        # self.wifi_ssid = info.get(const.ATTR_WIFI_SSID, {})
        # self.wifi_strength = info.get(const.ATTR_WIFI_STRENGTH, {})
        # self.total_power_import_t1_kwh = info.get(
        #     const.ATTR_TOTAL_POWER_IMPORT_T1_KWH, {}
        # )
        # self.total_power_import_t2_kwh = info.get(
        #     const.ATTR_TOTAL_POWER_IMPORT_T2_KWH, {}
        # )
        # self.total_power_export_t1_kwh = info.get(
        #     const.ATTR_TOTAL_POWER_EXPORT_T1_KWH, {}
        # )
        # self.total_power_export_t2_kwh = info.get(
        #     const.ATTR_TOTAL_POWER_EXPORT_T2_KWH, {}
        # )
        # self.active_power_w = info.get(const.ATTR_ACTIVE_POWER_W, {})
        # self.active_power_l1_w = info.get(const.ATTR_ACTIVE_POWER_L1_W, {})
        # self.active_power_l2_w = info.get(const.ATTR_ACTIVE_POWER_L2_W, {})
        # self.active_power_l3_w = info.get(const.ATTR_ACTIVE_POWER_L3_W, {})
        # self.total_gas_m3 = info.get(const.ATTR_TOTAL_GAS_M3, {})
        # self.gas_timestamp = info.get(const.ATTR_GAS_TIMESTAMP, {})

    # Async wrappers.
    async def async_update(self):
        _LOGGER.debug(f"{self.entity_id}.async_update called")
        await self.hass.async_add_job(self.update)
