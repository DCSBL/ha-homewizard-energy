"""The Homewizard Energy integration."""
import asyncio
import logging
import re
from enum import unique

import aiohwenergy
import async_timeout
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.util import slugify

from .const import (
    CONF_API,
    CONF_OVERRIDE_POLL_INTERVAL,
    CONF_POLL_INTERVAL_SECONDS,
    CONF_UNLOAD_CB,
    DEFAULT_OVERRIDE_POLL_INTERVAL,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DOMAIN,
)

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


async def migrate_old_configuration(hass: HomeAssistant, entry: ConfigEntry):
    """
    Migrates 0.4.x configuration, where unique_id was based on IP to
            >0.5.0 configuration, where unique_id is based on the serial ID
    """
    Logger.info("Migrating old integration to new one")

    host_ip = entry.unique_id
    api = aiohwenergy.HomeWizardEnergy(host_ip)
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

    if api.device == None:
        Logger.error(
            "Device (%s) API disabled, enable API and restart integration" % host_ip
        )
        return False

    # Update unique_id information
    unique_id = "%s_%s" % (
        api.device.product_type,
        api.device.serial,
    )

    # Update entities
    er = await entity_registry.async_get_registry(hass)
    entities = entity_registry.async_entries_for_config_entry(er, entry.entry_id)
    old_unique_id_prefix = "p1_meter_%s_" % slugify(host_ip)

    for entity in entities:
        new_unique_id_type = entity.unique_id.replace(old_unique_id_prefix, "")
        new_unique_id = "%s_%s" % (unique_id, new_unique_id_type)
        Logger.debug("Changing %s to %s" % (entity.unique_id, new_unique_id))
        er.async_update_entity(entity.entity_id, new_unique_id=new_unique_id)

    # Update device information
    data = entry.data.copy()
    data["host"] = host_ip
    data["name"] = api.device.product_name
    data["custom_name"] = api.device.product_name
    data["unique_id"] = unique_id
    data.pop("ip_address")

    hass.config_entries.async_update_entry(entry, data=data, unique_id=unique_id)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Homewizard Energy from a config entry."""

    Logger.debug("__init__ async_setup_entry")

    hass.data[DOMAIN][entry.data["unique_id"]] = {}

    # Migrate manual config to zeroconf (<0.5.0 to 0.5.x)
    # Check if unique_id == ipv4 or ipv6
    if re.match("(?:[0-9]{1,3}\.){3}[0-9]{1,3}", entry.unique_id) or re.match(
        "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
        entry.unique_id,
    ):
        result = await migrate_old_configuration(hass, entry)
        if not result:
            return False

    hass.data[DOMAIN][entry.data["unique_id"]][
        CONF_UNLOAD_CB
    ] = entry.add_update_listener(async_entry_updated)

    energy_api = aiohwenergy.HomeWizardEnergy(entry.data.get("host"))
    hass.data[DOMAIN][entry.data["unique_id"]][CONF_API] = energy_api
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_entry_updated(hass, config_entry):
    """Handle entry updates."""
    Logger.info("Configuration changed, reloading...")
    await hass.config_entries.async_reload(config_entry.entry_id)


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

    if unload_ok:
        config_data = hass.data[DOMAIN].pop(entry.data["unique_id"])
        if "api" in config_data:
            energy_api = config_data[CONF_API]
            await energy_api.close()

        if CONF_UNLOAD_CB in config_data:
            unload_cb = config_data[CONF_UNLOAD_CB]
            unload_cb()

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    Logger.debug("__init async_remove_entry")
    pass
