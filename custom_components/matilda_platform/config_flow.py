"""Config flow for Matilda Platform integration."""
import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .api import MatildaPlatformAPI
from .const import CONF_DISTRIBUTOR_ID, CONF_DISTRIBUTOR_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class MatildaPlatformConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Matilda Platform."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step - let user choose school."""
        if user_input is not None:
            # Validate the selection
            distributor_id = user_input[CONF_DISTRIBUTOR_ID]
            distributor_name = user_input[CONF_DISTRIBUTOR_NAME]

            # Check if distributor is already configured
            await self.async_set_unique_id(distributor_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=distributor_name,
                data={
                    CONF_DISTRIBUTOR_ID: distributor_id,
                    CONF_DISTRIBUTOR_NAME: distributor_name,
                },
            )

        # Fetch list of distributors
        distributors = await self._fetch_distributors()

        if not distributors:
            return self.async_abort(reason="cannot_connect")

        # Create schema with distributor choices
        distributor_options = {
            dist["id"]: f"{dist['name']} ({dist.get('address', {}).get('addressLocality', 'N/A')})"
            for dist in distributors
        }

        schema = vol.Schema(
            {
                vol.Required(CONF_DISTRIBUTOR_ID): vol.In(distributor_options),
                vol.Required(CONF_DISTRIBUTOR_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={
                "distributors_count": str(len(distributors))
            },
        )

    async def async_step_import(self, import_data: Dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_data)

    async def _fetch_distributors(self) -> list[Dict[str, Any]]:
        """Fetch list of distributors from API."""
        try:
            async with aiohttp.ClientSession() as session:
                api = MatildaPlatformAPI(session)
                distributors = await api.get_distributors()
                # Sort by name
                return sorted(distributors, key=lambda x: x.get("name", ""))
        except Exception as err:
            _LOGGER.error("Error fetching distributors: %s", err)
            return []
