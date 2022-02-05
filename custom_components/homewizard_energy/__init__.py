"""The Homewizard Energy integration."""
import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, TARGET_DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Homewizard Energy from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug("__init__ async_setup_entry")
    _LOGGER.warning("Sending config entry to core...")

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            TARGET_DOMAIN,
            context={"source": SOURCE_IMPORT, "old_config_entry_id": entry.entry_id},
            data=entry.data,
        )
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("__init__ async_unload_entry")

    return True
