"""HomeWizard Energy P1 meter integration."""

import logging
from datetime import timedelta

import async_timeout
import voluptuous
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers import config_validation
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import api as hw_api
from . import const, sensor, services

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = config_validation.PLATFORM_SCHEMA.extend(
    {
        voluptuous.Required(const.CONF_IP_ADDRESS): config_validation.string,
        voluptuous.Optional(const.CONF_NAME): config_validation.string,
    }
)


async def async_setup(hass, config):
    hass.data[const.DOMAIN] = {}
    return True


async def async_setup_entry(hass, entry):
    """Config entry example."""
    # assuming API object stored here by __init__.py

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True