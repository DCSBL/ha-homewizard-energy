"""HomeWizard Energy P1 meter integration."""

from datetime import timedelta
import logging
import async_timeout

from homeassistant.helpers import config_validation
import voluptuous

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import const
from . import services
from . import api as hw_api
from . import sensor

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
