"""Config flow for Homewizard Energy."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for P1 meter."""

    VERSION = 1

    def __init__(self):
        """Set up the instance."""
        _LOGGER.debug("config_flow __init__")

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""

        _LOGGER.debug("config_flow async_step_user")

        return self.async_abort(reason="manual_not_supported")
