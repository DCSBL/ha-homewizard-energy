"""Code to handle a Energy device Sync Box."""
import asyncio
import logging


import aiohwenergy
import async_timeout
import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.exceptions import ConfigEntryNotReady

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

from .const import DOMAIN, MANUFACTURER_NAME
from .errors import AuthenticationRequired, CannotConnect

Logger = logging.getLogger(__package__)


class HwEnergyDevice:
    """Manages a single Homewizard Energy device."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        """Initialize the system."""
        
        Logger.info("HwEnergyDevice %s" % config_entry.data["host"])
        
        self.config_entry = config_entry
        self.hass = hass
        self.api = None  # aiohwenergy instance
        self.entity = None  # Sensor entity

    def __str__(self):
        output = ""
        output += f"{self.config_entry}\n"
        output += f"{self.api}\n"
        output += f"{self.entity}\n"
        return output

    async def async_setup(self, tries=0):
        """Set up a Home Wizard Energy device."""
        hass = self.hass

        initialized = False
        try:
            self.api = await async_get_aiohwenergy_from_entry_data(
                self.config_entry.data
            )
            with async_timeout.timeout(10):
                await self.api.initialize()
                await self.async_update_registered_device_info()  # Info might have changed while HA was not running
                initialized = True
        except (asyncio.TimeoutError, aiohwenergy.RequestError):
            Logger.error(
                "Error connecting to the Energy device at %s",
                self.config_entry.data["host"],
            )
            raise ConfigEntryNotReady
        except aiohwenergy.AioHwEnergyException:
            Logger.exception("Unknown Energy API error occurred")
            raise ConfigEntryNotReady
        except Exception:  # pylint: disable=broad-except
            Logger.exception(
                "Unknown error connecting with Energy Device at %s",
                self.config_entry.data["host"],
            )
            return False
        finally:
            if not initialized:
                await self.api.close()

        hwenergy = self  # Alias for use in async_stop

        async def async_stop(self, event=None) -> None:
            """Unsubscribe from events."""
            await hwenergy.async_reset()

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_stop)

        return True

    async def async_reset(self):
        """
        Reset this energy device to default state.
        """
        if self.api is not None:
            await self.api.close()

        return True

    async def async_update_registered_device_info(self):
        """
        Update device registry with info from the API
        """
        if self.api is not None:
            device_registry = (
                await self.hass.helpers.device_registry.async_get_registry()
            )
            # Get or create also updates existing entries
            device_registry.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, self.api.device.unique_id)},
                name=self.api.device.product_name,
                manufacturer=MANUFACTURER_NAME,
                model=self.api.device.product_type,
                sw_version=self.api.device.firmware_version,
            )

            # Title formatting is actually in the translation file, but don't know how to get it from here.
            # Actually it being in the translation is a bit weird anyway since the frontend can be different language
            self.hass.config_entries.async_update_entry(
                self.config_entry,
                title=f"{self.api.device.name} ({self.api.device.unique_id})",
            )

        return True


async def async_register_aiohwenergy(hass, api):
    try:
        with async_timeout.timeout(30):
            registration_info = None
            while not registration_info:
                try:
                    registration_info = await api.register(
                        "Home Assistant", hass.config.location_name
                    )
                except aiohwenergy.InvalidState:
                    # This is expected as syncbox will be in invalid state until button is pressed
                    pass
                await asyncio.sleep(1)
            return registration_info
    except (asyncio.TimeoutError, aiohwenergy.Unauthorized):
        raise AuthenticationRequired
    except aiohwenergy.RequestError:
        raise CannotConnect
    except aiohwenergy.AioHwEnergyException:
        Logger.exception("Unknown HomeWizard Energy error occurred")
        raise CannotConnect


async def async_get_aiohwenergy_from_entry_data(entry_data):
    """Create a HwEnergyDevice object from entry data."""

    Logger.debug(
        "%s async_get_aiohwenergy_from_entry_data\nentry_data:\n%s"
        % (__name__, str(entry_data))
    )

    return aiohwenergy.HomeWizardEnergy(
        entry_data["host"],
    )
