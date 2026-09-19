"""Sensor platform for Matilda Platform."""
import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .api import MatildaPlatformAPI
from .const import CONF_DISTRIBUTOR_ID, CONF_DISTRIBUTOR_NAME, DOMAIN, SCAN_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)


class MatildaPlatformMenuSensor(SensorEntity):
    """Sensor for displaying today's menu from Matilda Platform."""

    def __init__(
        self,
        api: MatildaPlatformAPI,
        distributor_id: str,
        distributor_name: str,
    ):
        """Initialize the sensor."""
        self._api = api
        self._distributor_id = distributor_id
        self._distributor_name = distributor_name
        self._state = None
        self._attr_unique_id = f"matilda_platform_{distributor_id}_menu"
        self._attr_name = f"{distributor_name} - Meny idag"
        self._attr_icon = "mdi:food"
        self._attr_native_unit_of_measurement = None
        self._last_update = None

    @property
    def native_value(self) -> str:
        """Return the current menu as state."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        return {
            "distributor_id": self._distributor_id,
            "distributor_name": self._distributor_name,
            "last_update": self._last_update,
        }

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        await self.async_update()

        # Schedule hourly updates
        def schedule_update(_now):
            """Schedule update."""
            asyncio.create_task(self.async_update())

        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                schedule_update,
                timedelta(hours=SCAN_INTERVAL_HOURS),
            )
        )

    async def async_update(self) -> None:
        """Fetch and update the menu."""
        try:
            menu_data = await self._api.get_menu(self._distributor_id)
            menu_text = self._api.parse_menu(menu_data)
            self._state = menu_text
            self._last_update = datetime.now().isoformat()
            _LOGGER.debug(
                "Updated menu for %s: %s", self._distributor_name, menu_text
            )
        except Exception as err:
            _LOGGER.error("Error updating menu for %s: %s", self._distributor_name, err)
            self._state = "Kunde inte läsa in meny"
            self._last_update = datetime.now().isoformat()

        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Matilda Platform sensor."""
    data = hass.data[DOMAIN][config_entry.entry_id]

    sensor = MatildaPlatformMenuSensor(
        api=data["api"],
        distributor_id=data["distributor_id"],
        distributor_name=data["distributor_name"],
    )

    async_add_entities([sensor])
