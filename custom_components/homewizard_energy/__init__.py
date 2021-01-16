"""The Homewizard Energy integration."""
import asyncio
import logging
import re

import voluptuous as vol
import aiohwenergy
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

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
    
    # Migrate manual config to zeroconf (<0.5.0 to 0.5.x)
    if re.match("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", entry.unique_id):
        Logger.info("Converting old integration to new one")
        
        host_ip = entry.unique_id
        api = aiohwenergy.HomeWizardEnergy("192.168.107.108")
        
        try:
            with async_timeout.timeout(5):
                await api.initialize()
        except (asyncio.TimeoutError, aiohwenergy.RequestError):
            Logger.error(
                "(-1) Error connecting to the Energy device at %s",
                host_ip,
            )
            return False
        except Exception:  # pylint: disable=broad-except
            Logger.error(
                "(-2) Error connecting to the Energy device at %s",
                host_ip,
            )
            return False
        finally:
            await api.close()
        
        # Logger.info(api)
        # Logger.info(api.device)
        if (api.device == None):
            Logger.error("Device (%s) API disabled, enable API and restart integration" % host_ip)
            return False
          
        # Update device information  
        unique_id = "%s_%s" % (
            api.device.product_type,
            api.device.serial,
        )
        
        Logger.info("Unique id = %s" % unique_id)
        
        # Logger.info(entry.data)
        # Logger.info(host_ip)
        data = entry.data.copy()
        data["host"] = host_ip
        data["name"] = api.device
        data["custom_name"] = host_ip
        # data.pop("ip_address")
        
        hass.config_entries.async_update_entry(entry, data=data)
        
        # energydevice = HwEnergyDevice(hass, entry)
        # print(energydevice)
        # await energydevice.async_setup()
        
        # hass.config_entries.async_update_entry(entry)

    # energydevice = HwEnergyDevice(hass, entry)
    # return False
    
    # hass.data[DOMAIN][entry.data["unique_id"]] = energydevice

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
    Logger.debug("__init async_remove_entry")
    pass
