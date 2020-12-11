"""Creates Homewizard Energy sensor entities."""

from .aiohwenergy import aiohwenergy
import logging
import async_timeout

from datetime import timedelta

from homeassistant.const import (
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    POWER_WATT,
    VOLUME_CUBIC_METERS,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import const

Logger = logging.getLogger(__name__)

_PLATFORM = "sensor"

SENSORS = {
    # const.ATTR_SMR_VERSION: {"icon": "mdi:pound", "unit": ""},
    # const.ATTR_METER_MODEL: {"icon": "mdi:counter", "unit": ""},
    # const.ATTR_WIFI_SSID: {"icon": "mdi:wifi", "unit": ""},
    # const.ATTR_WIFI_STRENGTH: {"icon": "mdi:wifi", "unit": PERCENTAGE},
    # const.ATTR_TOTAL_POWER_IMPORT_T1_KWH: {
    #     "icon": "mdi:home-import-outline",
    #     "unit": ENERGY_KILO_WATT_HOUR,
    # },
    # const.ATTR_TOTAL_POWER_IMPORT_T2_KWH: {
    #     "icon": "mdi:home-import-outline",
    #     "unit": ENERGY_KILO_WATT_HOUR,
    # },
    # const.ATTR_TOTAL_POWER_EXPORT_T1_KWH: {
    #     "icon": "mdi:home-export-outline",
    #     "unit": ENERGY_KILO_WATT_HOUR,
    # },
    # const.ATTR_TOTAL_POWER_EXPORT_T2_KWH: {
    #     "icon": "mdi:home-export-outline",
    #     "unit": ENERGY_KILO_WATT_HOUR,
    # },
    const.ATTR_ACTIVE_POWER_W: {"icon": "mdi:transmission-tower", "unit": POWER_WATT},
    # const.ATTR_ACTIVE_POWER_L1_W: {
    #     "icon": "mdi:transmission-tower",
    #     "unit": POWER_WATT,
    # },
    # const.ATTR_ACTIVE_POWER_L2_W: {
    #     "icon": "mdi:transmission-tower",
    #     "unit": POWER_WATT,
    # },
    # const.ATTR_ACTIVE_POWER_L3_W: {
    #     "icon": "mdi:transmission-tower",
    #     "unit": POWER_WATT,
    # },
    # const.ATTR_TOTAL_GAS_M3: {"icon": "mdi:fire", "unit": VOLUME_CUBIC_METERS},
    # const.ATTR_GAS_TIMESTAMP: {"icon": "mdi:timeline-clock", "unit": ""},
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""
    Logger.info("Setting up sensor for HomeWizard Energy.")

    energy_api = aiohwenergy.HomeWizardEnergy(entry.data["host"])
    
    await energy_api.initialize()

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with async_timeout.timeout(10):
            try:
                await energy_api.data.update()
                
                new_data = {}
                for entry_point in SENSORS:
                    new_data[entry_point] = getattr(energy_api.data, entry_point)
                
                return new_data
            except AttributeError:
                return
    
    # Determine update interval
    ## Default update interval
    update_interval = 5
    
    try:
        product_type = energy_api.device.product_type
    except AttributeError:
        product_type = "Unknown"
        
    if (product_type == "HWE-P1"):
        try:
            smr_version = energy_api.data.smr_version
            if (smr_version == 50):
                update_interval = 5 # TODO set back to 1, Throttle down for now, 
            else:
                update_interval = 5
        except AttributeError:
            pass
        
    if (product_type == "SDM230-wifi" or product_type == "SDM630-wifi"):
        update_interval = 1
    
    coordinator = DataUpdateCoordinator(
        hass,
        Logger,
        # Name of the data. For logging purposes.
        name=entry.data["product_name"],
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=update_interval),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    # services.register_services(hass)
    async_add_entities(
        device_hwe_p1(coordinator, entry.data, info_type)
        for info_type in SENSORS
    )

    return True

class device_hwe_p1(CoordinatorEntity):
    """Representation of a HomeWizard Energy"""
    
    host = None
    name = None
    unique_id = None
    entry_data = None

    def __init__(self, coordinator, entry_data, info_type):
        """Initializes the sensor."""

        super().__init__(coordinator)

        # Config attributes.
        self.name = f"{ entry_data['product_name'] } {info_type}"
        
        self.api = None

        self.host = entry_data["host"]
        self.info_type = info_type
        self.coordinator = coordinator
        self.entry_data = entry_data
        self.unique_id = f"{ entry_data['product_type'] }_{entry_data['unique_id']}_{info_type}"

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

async def async_get_aiohwenergy_from_entry_data(entry_data):
    """Create a HomewizardEnergy object from entry data."""

    Logger.debug(
        "%s async_get_aiohuesyncbox_from_entry_data\nentry_data:\n%s"
        % (__name__, str(entry_data))
    )

    return aiohwenergy.HomeWizardEnergy (
        entry_data["host"]
    )