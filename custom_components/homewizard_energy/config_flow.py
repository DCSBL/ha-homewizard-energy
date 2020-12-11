"""Config flow for Homewizard Energy."""
import aiohwenergy

import logging
from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

Logger = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for P1 meter."""
    
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    
    def __init__(self):
        """Set up the instance."""
        Logger.debug("config_flow __init__")
        
    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        Logger.debug("config_flow async_step_user")
        return self.async_abort(reason="manual_not_supported")
        
    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery."""

        Logger.debug("config_flow async_step_zeroconf")
        Logger.debug(discovery_info["properties"])
        
        entry_info = {
            "host": discovery_info["host"],
            "port": discovery_info["port"],
            "api_enabled": discovery_info["properties"]['api_enabled'] if 'api_enabled' in discovery_info["properties"] else None,
            "path": discovery_info["properties"]['path'] if 'path' in discovery_info["properties"] else None,
            "product_name": discovery_info["properties"]['product_name'] if 'product_name' in discovery_info["properties"] else None,
            "product_type": discovery_info["properties"]['product_type'] if 'product_type' in discovery_info["properties"] else None,
            "unique_id": discovery_info["properties"]['serial'] if 'serial' in discovery_info["properties"] else None
        }

        Logger.debug(f"Found info: { entry_info['host'] } { entry_info['unique_id'] }.")

        return await self.async_step_check(entry_info)
        
    async def async_step_check(self, entry_info):
        """Perform some checks and create entry if OK."""
        
        Logger.debug("config_flow async_step_check")

        await self.async_set_unique_id(entry_info["unique_id"])
        self._abort_if_unique_id_configured(updates=entry_info)

        if entry_info["api_enabled"] != "1":
            Logger.warning("API not enabled")
            return self.async_abort(reason="api_not_enabled")
        
        Logger.debug(f"entry_info: {entry_info}")
        
        if ((entry_info["host"] == None) or
            (entry_info["port"] == None) or
            (entry_info["unique_id"] == None) or
            (entry_info["product_name"] == None) or
            (entry_info["product_type"] == None) or
            (entry_info["path"] == None) or
            (entry_info["api_enabled"] == None)):
            Logger.warning(f"Invalid discovery parameters")
            return self.async_abort(reason="invalid_discovery_parameters")
            
        self.context["host"] = entry_info["host"]
        self.context["unique_id"] = entry_info["unique_id"]
        self.context["port"] = entry_info["port"]
        self.context["product_name"] = entry_info["product_name"]
        self.context["path"] = entry_info["path"]
        self.context["product_type"] = entry_info["product_type"]
        self.context["api_enabled"] = entry_info["api_enabled"]

        self.context["title_placeholders"] = {
            "name": self.context["product_name"],
            "unique_id": self.context["unique_id"],
        }

        # api = await async_get_aiohuesyncbox_from_entry_data(entry_info)
        # if await api.is_registered():
        #     await api.close()
        # return await self._async_create_entry_from_context()

        return await self.async_step_discovery_confirm()
        
    async def async_step_discovery_confirm(self, user_input=None):
        """Handle user-confirmation of discovered node."""
        
        Logger.debug("config_flow async_step_discovery_confirm")
        
        errors = {}
        
        if self.context["api_enabled"] != "1":
            Logger.warning(f"API not enabled")
            errors["base"] = "api_not_enabled"
            return self.async_show_form(step_id="discovery_confirm", errors=errors)
        
        if user_input is None:
            Logger.debug("async_step_discovery_confirm user_input is None")
            return self.async_show_form(
                step_id="discovery_confirm",
                description_placeholders={"name": "aaabbbccc"},
            )
        
        Logger.debug("async_step_discovery_confirm _create_entry")
        
        return self.async_create_entry(
            title=self.context["product_name"],
            data=self.context,
        )

# async def _async_has_devices(hass) -> bool:
#     """Return if there are devices that can be discovered."""
#     # TODO Check if there are any devices that can be discovered in the network.
#     devices = await hass.async_add_executor_job(aiohwenergy.discover)
#     return len(devices) > 0


# config_entry_flow.register_discovery_flow(
#     DOMAIN, "Homewizard Energy", _async_has_devices, config_entries.CONN_CLASS_UNKNOWN
# )
