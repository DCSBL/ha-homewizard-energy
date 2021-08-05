"""Creates Homewizard Energy switch entities."""

from config.custom_components.homewizard_energy import Logger
from homeassistant.const import CONF_STATE
from typing import Any, Final

import aiohwenergy

from homeassistant.components.switch import (
    DEVICE_CLASS_OUTLET,
    DEVICE_CLASS_SWITCH,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import DOMAIN, HomeAssistant
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from homeassistant.const import CONF_ID

from .const import (
    ATTR_POWER_ON,
    ATTR_SWITCHLOCK,
    CONF_MODEL,
    CONF_SW_VERSION,
    COORDINATOR,
    DOMAIN,
    CONF_API,
)

SWITCHES: Final[list[SwitchEntityDescription]] = [
    SwitchEntityDescription(
        key=ATTR_POWER_ON, name="On", device_class=DEVICE_CLASS_OUTLET
    ),
    SwitchEntityDescription(
        key=ATTR_SWITCHLOCK,
        name="Switch lock",
        device_class=DEVICE_CLASS_SWITCH,
        icon="mdi:lock",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switches."""

    energy_api = hass.data[DOMAIN][entry.data["unique_id"]][CONF_API]
    coordinator = hass.data[DOMAIN][entry.data["unique_id"]][COORDINATOR]

    if energy_api.state != None:
        entities = []
        for description in SWITCHES:
            entities.append(
                HWEnergySwitch(coordinator, entry.data, description, energy_api)
            )

        async_add_entities(entities)


class HWEnergySwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a HomeWizard Energy Switch"""

    unique_id = None
    name = None

    def __init__(self, coordinator, entry_data, description, api) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self.coordinator = coordinator
        self.entry_data = entry_data
        self.api = api

        # Config attributes
        self.name = "%s %s" % (entry_data["custom_name"], description.name)
        self.unique_id = "%s_%s" % (entry_data["unique_id"], description.key)
        self.data_type = description.key

    @property
    def data(self) -> dict[str, Any]:
        """Return data from DataUpdateCoordinator."""
        return self.coordinator.data

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return {
            "name": self.entry_data["custom_name"],
            "manufacturer": "HomeWizard",
            "sw_version": self.data[CONF_SW_VERSION],
            "model": self.data[CONF_MODEL],
            "identifiers": {(DOMAIN, self.data[CONF_ID])},
        }

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.data[CONF_STATE][self.data_type]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if self.data_type == ATTR_POWER_ON:
            await self.api.state.set(power_on=True)
        elif self.data_type == ATTR_SWITCHLOCK:
            await self.api.state.set(switch_lock=True)
        else:
            Logger.error("Internal error, unknown action")

        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self.data_type == ATTR_POWER_ON:
            await self.api.state.set(power_on=False)
        elif self.data_type == ATTR_SWITCHLOCK:
            await self.api.state.set(switch_lock=False)
        else:
            Logger.error("Internal error, unknown action")

        await self.coordinator.async_refresh()
