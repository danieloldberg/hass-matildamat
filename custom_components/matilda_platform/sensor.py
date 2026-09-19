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


class MatildaPlatformMealSensor(SensorEntity):
    """Sensor for displaying a specific meal from Matilda Platform."""

    def __init__(
        self,
        api: MatildaPlatformAPI,
        distributor_id: str,
        distributor_name: str,
        meal_name: str,
    ):
        """Initialize the sensor."""
        self._api = api
        self._distributor_id = distributor_id
        self._distributor_name = distributor_name
        self._meal_name = meal_name
        self._state = None
        self._courses = []
        
        # Create unique ID and name
        meal_slug = meal_name.lower().replace(" ", "_").replace("å", "a").replace("ä", "a").replace("ö", "o")
        self._attr_unique_id = f"matilda_platform_{distributor_id}_{meal_slug}"
        self._attr_name = f"{distributor_name} - {meal_name}"
        self._attr_icon = "mdi:food"
        self._last_update = None

    @property
    def native_value(self) -> str:
        """Return the current meal courses as state."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        return {
            "distributor_id": self._distributor_id,
            "distributor_name": self._distributor_name,
            "meal_name": self._meal_name,
            "courses": self._courses,
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
            parsed_menu = self._api.parse_menu(menu_data)
            
            # Find the meal by name
            meal_found = False
            for meal in parsed_menu.get("meals", []):
                if meal.get("name") == self._meal_name:
                    self._courses = meal.get("courses", [])
                    # Format courses as bullet points
                    if self._courses:
                        self._state = "\n".join([f"• {course}" for course in self._courses])
                    else:
                        self._state = "Ingen rätt"
                    meal_found = True
                    break
            
            if not meal_found:
                self._state = "Ingen meny idag"
                self._courses = []
            
            self._last_update = datetime.now().isoformat()
            _LOGGER.debug(
                "Updated %s for %s: %s", self._meal_name, self._distributor_name, self._state
            )
        except Exception as err:
            _LOGGER.error(
                "Error updating %s for %s: %s", self._meal_name, self._distributor_name, err
            )
            self._state = "Kunde inte läsa in meny"
            self._courses = []
            self._last_update = datetime.now().isoformat()

        self.async_write_ha_state()


class MatildaPlatformSummaryMenuSensor(SensorEntity):
    """Summary sensor showing all meals for the day."""

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
        self._meals = []
        
        self._attr_unique_id = f"matilda_platform_{distributor_id}_meny_idag"
        self._attr_name = f"{distributor_name} - Meny idag"
        self._attr_icon = "mdi:food"
        self._last_update = None

    @property
    def native_value(self) -> str:
        """Return summary of all meals."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes with full meal structure."""
        return {
            "distributor_id": self._distributor_id,
            "distributor_name": self._distributor_name,
            "meals": self._meals,
            "meal_count": len(self._meals),
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
            parsed_menu = self._api.parse_menu(menu_data)
            
            self._meals = parsed_menu.get("meals", [])
            
            if not self._meals:
                self._state = "Ingen meny idag"
            else:
                # Format all meals
                meal_lines = []
                for meal in self._meals:
                    meal_name = meal.get("name", "")
                    courses = meal.get("courses", [])
                    meal_lines.append(f"**{meal_name}:**")
                    for course in courses:
                        meal_lines.append(f"• {course}")
                    meal_lines.append("")  # Empty line between meals
                
                self._state = "\n".join(meal_lines).strip()
            
            self._last_update = datetime.now().isoformat()
            _LOGGER.debug(
                "Updated summary menu for %s with %d meals", 
                self._distributor_name, 
                len(self._meals)
            )
        except Exception as err:
            _LOGGER.error(
                "Error updating summary menu for %s: %s", self._distributor_name, err
            )
            self._state = "Kunde inte läsa in meny"
            self._meals = []
            self._last_update = datetime.now().isoformat()

        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Matilda Platform sensors."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    
    distributor_id = data["distributor_id"]
    distributor_name = data["distributor_name"]
    api = data["api"]
    
    # Fetch menu once to get meal names
    menu_data = await api.get_menu(distributor_id)
    parsed_menu = api.parse_menu(menu_data)
    
    sensors = []
    
    # Create summary sensor (always)
    summary_sensor = MatildaPlatformSummaryMenuSensor(
        api=api,
        distributor_id=distributor_id,
        distributor_name=distributor_name,
    )
    sensors.append(summary_sensor)
    
    # Create a sensor for each meal type found
    meal_names = set()
    for meal in parsed_menu.get("meals", []):
        meal_name = meal.get("name", "").strip()
        if meal_name and meal_name not in meal_names:
            meal_names.add(meal_name)
            sensor = MatildaPlatformMealSensor(
                api=api,
                distributor_id=distributor_id,
                distributor_name=distributor_name,
                meal_name=meal_name,
            )
            sensors.append(sensor)
    
    # If no meals found, just use the summary sensor
    if not meal_names:
        _LOGGER.warning("No meals found for %s", distributor_name)
    
    async_add_entities(sensors)


