"""Defines services that HomeWizard Energy P1 component supports."""

import logging
import voluptuous

from homeassistant.helpers import config_validation
from homeassistant.helpers import service

from . import const

_LOGGER = logging.getLogger(__name__)


def register_services(hass):
    """Registers custom services for homewizard_energy_p1."""
    _LOGGER.debug("Registering services for HomeWizard Energy P1.")


def unregister_services(hass):
    """Unregisters custom services from homewizard_energy_p1."""