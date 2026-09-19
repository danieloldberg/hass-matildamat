"""Matilda Platform integration."""
import asyncio
import logging
from datetime import datetime, timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change

from .api import MatildaPlatformAPI
from .const import CONF_DISTRIBUTOR_ID, CONF_DISTRIBUTOR_NAME, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Matilda Platform from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API client
    session = async_get_clientsession(hass)
    api = MatildaPlatformAPI(session)

    # Store API instance
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "distributor_id": entry.data[CONF_DISTRIBUTOR_ID],
        "distributor_name": entry.data[CONF_DISTRIBUTOR_NAME],
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Schedule update at midnight
    async def midnight_update(now):
        """Update at midnight."""
        _LOGGER.debug("Running scheduled midnight update for %s", entry.title)
        # Dispatch update to sensor
        hass.async_create_task(
            hass.config_entries.async_reload(entry.entry_id)
        )

    # Track time at 00:00 every day
    hass.data[DOMAIN][entry.entry_id]["unsub_midnight"] = async_track_time_change(
        hass, midnight_update, hour=0, minute=0, second=0
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove scheduled update
    if entry.entry_id in hass.data[DOMAIN]:
        unsub = hass.data[DOMAIN][entry.entry_id].get("unsub_midnight")
        if unsub:
            unsub()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
