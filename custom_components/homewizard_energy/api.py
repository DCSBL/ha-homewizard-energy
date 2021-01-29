"""Creates class to interact with HomeWizard Energy P1 meter API.

API Documentation: https://energy.homewizard.net/en/support/solutions/articles/19000117051-homewizard-p1-meter-local-api-beta-
"""

import enum
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)


class HWEP1Endpoints(enum.Enum):
    """HomeWizard Energy P1 API endpoints."""

    ENERGY_DATA = "api/v1/data"
    # TELEGRAM_DATA = "api/v1/telegram"


class HWEP1Api(object):
    """Class to interact with HomeWizard Energy P1 meter API.

    Public Methods:
      get_energy_data: Gets energy data
    """

    def __init__(self, ip_address):
        """Initializes API service.

        Args:
          ip_address: IP of the P1 meter
        """
        self._ip_address = ip_address
        _LOGGER.debug(f"HomeWizard Energy P1 meter with IP {ip_address} initialized.")

    # Public methods.
    async def get_energy_data(self):
        """Gets energy data

        Returns:
          Dictionary containing device information.
        """
        return await self._call_api_endpoint(HWEP1Endpoints.ENERGY_DATA)
        # return response

    # Helpers.
    def _get_api_url(self, api_endpoint):
        """Gets URL for a given endpoint and JSON payload.

        Args:
          api_endpoint: P1 endpoint to call.

        Returns:
          API URL.
        """
        return "http://{ip}/{endpoint}".format(
            ip=self._ip_address,
            endpoint=api_endpoint.value,
        )

    async def _call_api_endpoint(self, api_endpoint, payload=None):
        """Makes a call to the HomeWizard Energy endpoint

        Args:
          api_endpoint: HWEP1Endpoints to call.
          payload: Payload to send to API call.

        Returns:
          API response in dict format.
        """
        api_url = self._get_api_url(api_endpoint)
        api_headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

        if api_endpoint == HWEP1Endpoints.ENERGY_DATA:

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=api_headers, timeout=30) as r:
                    response = await r.json()
        else:
            raise NotImplementedError("Unknown API endpoint.")

        _LOGGER.debug(f"Received body: {response}")

        return response