"""The Homewizard Energy integration."""
import asyncio
import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .energydevice import HwEnergyDevice

Logger = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Homewizard Energy component."""
    Logger.debug("__init__ async_setup")
    hass.data[DOMAIN] = {}

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Homewizard Energy from a config entry."""

    Logger.debug("__init__ async_setup_entry")

    energydevice = HwEnergyDevice(hass, entry)
    hass.data[DOMAIN][entry.data["unique_id"]] = energydevice

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    Logger.debug("__init__ async_unload_entry")

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    Logger.warning(
        "Unloading component not fully developed, restart Home Assistant to fully unload component"
    )
    return False

    # if unload_ok:
    #     Logger.info(hass.data[DOMAIN])
    #     energydevice = hass.data[DOMAIN].pop(entry.data["unique_id"])
    #     await energydevice.api.close()

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    pass
