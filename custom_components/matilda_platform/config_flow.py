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
    
    def __init__(self):
        """Initialize the config flow."""
        super().__init__()
        self._distributors = []  # Cache distributors list

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step - search for school."""
        if user_input is not None:
            search_query = user_input.get("search_query", "").strip().lower()
            
            # Fetch distributors if not cached
            if not self._distributors:
                self._distributors = await self._fetch_distributors()
            
            if not self._distributors:
                return self.async_abort(reason="cannot_connect")
            
            # Filter distributors by search query
            if search_query:
                filtered = [
                    d for d in self._distributors
                    if search_query in d["name"].lower()
                ]
            else:
                filtered = self._distributors
            
            # If no results, show error
            if not filtered:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required("search_query"): str,
                    }),
                    description_placeholders={"info": "Ingen skola hittad. Försök med annat namn."},
                    errors={"base": "no_results"},
                )
            
            # If only one result, skip to selection
            if len(filtered) == 1:
                return await self.async_step_select_school()
            
            # Otherwise, show selection step with filtered results
            self.context["search_results"] = filtered
            return await self.async_step_select_school()
        
        # Show search form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("search_query"): str,
            }),
            description_placeholders={
                "info": "Sök efter skolans/förskolans namn. T.ex. 'Björkstaden' eller 'Montessori'"
            },
        )

    async def async_step_select_school(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle school selection from search results."""
        if user_input is not None:
            distributor_id = user_input.get("distributor_id")
            distributor = next(
                (d for d in self._distributors if d["id"] == distributor_id),
                None,
            )
            
            if not distributor:
                return self.async_abort(reason="selection_failed")
            
            # Check if already configured
            await self.async_set_unique_id(distributor["id"])
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=distributor["name"],
                data={
                    CONF_DISTRIBUTOR_ID: distributor["id"],
                    CONF_DISTRIBUTOR_NAME: distributor["name"],
                },
            )
        
        # Get search results from context
        search_results = self.context.get("search_results", [])
        
        if not search_results:
            # No results found
            return self.async_abort(reason="no_schools_found")
        
        # Build options: id -> "Name (City)"
        school_options = {
            dist["id"]: f"{dist['name']} ({dist.get('address', {}).get('addressLocality', 'N/A')})"
            for dist in search_results
        }
        
        schema = vol.Schema({
            vol.Required("distributor_id"): vol.In(school_options),
        })
        
        return self.async_show_form(
            step_id="select_school",
            data_schema=schema,
            description_placeholders={
                "count": str(len(search_results))
            },
        )

    async def async_step_import(self, import_data: Dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        # For YAML import, we need both ID and name
        if CONF_DISTRIBUTOR_ID in import_data and CONF_DISTRIBUTOR_NAME in import_data:
            distributor_id = import_data[CONF_DISTRIBUTOR_ID]
            distributor_name = import_data[CONF_DISTRIBUTOR_NAME]
            
            await self.async_set_unique_id(distributor_id)
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=distributor_name,
                data={
                    CONF_DISTRIBUTOR_ID: distributor_id,
                    CONF_DISTRIBUTOR_NAME: distributor_name,
                },
            )
        
        # If only ID provided, fetch name from API
        distributor_id = import_data.get(CONF_DISTRIBUTOR_ID)
        if distributor_id:
            self._distributors = await self._fetch_distributors()
            distributor = next(
                (d for d in self._distributors if d["id"] == distributor_id),
                None,
            )
            
            if distributor:
                await self.async_set_unique_id(distributor_id)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=distributor["name"],
                    data={
                        CONF_DISTRIBUTOR_ID: distributor_id,
                        CONF_DISTRIBUTOR_NAME: distributor["name"],
                    },
                )
        
        return self.async_abort(reason="import_failed")

    async def _fetch_distributors(self) -> list[Dict[str, Any]]:
        """Fetch list of distributors from API and sort by name."""
        try:
            async with aiohttp.ClientSession() as session:
                api = MatildaPlatformAPI(session)
                distributors = await api.get_distributors()
                # Sort alphabetically by name
                return sorted(distributors, key=lambda x: x.get("name", "").lower())
        except Exception as err:
            _LOGGER.error("Error fetching distributors: %s", err)
            return []

