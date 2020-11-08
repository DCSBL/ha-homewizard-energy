"""HomeWizard Energy P1 meter integration."""

import logging
import voluptuous
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers import config_validation

from . import const

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = config_validation.PLATFORM_SCHEMA.extend(
    {
        voluptuous.Required(const.CONF_IP_ADDRESS): config_validation.string,
        voluptuous.Optional(const.CONF_NAME): config_validation.string,
    }
)


async def async_setup(hass, config):
    hass.data[const.DOMAIN] = {}
    _LOGGER.info(f"---> Hello")
    return True


async def async_setup_entry(hass, entry):
    """Config entry example."""
    # assuming API object stored here by __init__.py

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


# async def get_coordinator(hass):
#     """Get the data update coordinator."""
#     if DOMAIN in hass.data:
#         return hass.data[DOMAIN]

#     async def async_get_status():
#         with async_timeout.timeout(10):
#             return {
#                 case.country: case
#                 for case in await self._api.get_energy_data().get_cases(
#                     aiohttp_client.async_get_clientsession(hass)
#                 )
#             }

#     hass.data[DOMAIN] = update_coordinator.DataUpdateCoordinator(
#         hass,
#         logging.getLogger(__name__),
#         name=DOMAIN,
#         update_method=async_get_cases,
#         update_interval=timedelta(hours=1),
#     )
#     await hass.data[DOMAIN].async_refresh()
#     return hass.data[DOMAIN]
