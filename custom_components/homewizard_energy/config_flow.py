"""Config flow for P1 meter."""

from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for P1 meter."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    _options = None

    def __init__(self):
        """Set up the instance."""

    async def async_step_user(
        self, user_input: Optional[ConfigType] = None
    ) -> Dict[str, Any]:
        """Handle a flow initiated by the user."""
        if user_input is None:
            return self._show_setup_form()

        unique_id = user_input[CONF_IP_ADDRESS]

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(
            updates={CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS]}
        )

        return self.async_create_entry(
            title=user_input[CONF_IP_ADDRESS], data=user_input
        )

    def _show_setup_form(self, errors: Optional[Dict] = None) -> Dict[str, Any]:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): str,
                }
            ),
            errors=errors or {},
        )
