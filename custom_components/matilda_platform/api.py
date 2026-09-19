"""Matilda Platform API client."""
import asyncio
import logging
import ssl
from datetime import datetime, timedelta
from typing import Any, Optional

import aiohttp

from .const import MATILDA_API_BASE, MATILDA_MENU_URL, MATILDA_DISTRIBUTORS_URL

_LOGGER = logging.getLogger(__name__)


class MatildaPlatformAPI:
    """Client for Matilda Platform API."""

    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.session = session
        # Create SSL context that allows self-signed certificates
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE

    async def get_distributors(self) -> list[dict[str, Any]]:
        """Fetch list of all distributors (schools)."""
        try:
            async with self.session.get(
                MATILDA_DISTRIBUTORS_URL,
                timeout=aiohttp.ClientTimeout(total=10),
                ssl=self._ssl_context,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("distributors", [])
                else:
                    _LOGGER.error(
                        "Failed to fetch distributors: HTTP %d", response.status
                    )
                    return []
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching distributors")
            return []
        except Exception as err:
            _LOGGER.error("Error fetching distributors: %s", err)
            return []

    async def get_menu(
        self,
        distributor_id: str,
        date: Optional[datetime] = None,
    ) -> dict[str, Any]:
        """
        Fetch menu for a specific distributor and date.

        Args:
            distributor_id: The distributor ID
            date: Date to fetch menu for (default: today)

        Returns:
            Dictionary with menu data
        """
        if date is None:
            date = datetime.now()

        start_date = date.strftime("%Y-%m-%d")
        end_date = date.strftime("%Y-%m-%d")

        params = {
            "distributorId": distributor_id,
            "startDate": start_date,
            "endDate": end_date,
            "lang": "sv",
        }

        try:
            async with self.session.get(
                MATILDA_MENU_URL,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
                ssl=self._ssl_context,
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error(
                        "Failed to fetch menu for %s: HTTP %d",
                        distributor_id,
                        response.status,
                    )
                    return {}
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching menu for distributor %s", distributor_id)
            return {}
        except Exception as err:
            _LOGGER.error(
                "Error fetching menu for distributor %s: %s", distributor_id, err
            )
            return {}

    def parse_menu(self, api_response: dict[str, Any]) -> str:
        """
        Parse menu data from API response.

        Args:
            api_response: Raw API response

        Returns:
            Formatted menu string
        """
        meals = api_response.get("meals", [])

        if not meals:
            return "Ingen meny idag"

        # Get first meal of the day
        first_meal = meals[0]
        courses = first_meal.get("courses", [])

        if not courses:
            return "Ingen meny idag"

        # Build menu text from all courses
        menu_items = []
        for course in courses:
            course_name = course.get("name", "").strip()
            if course_name:
                menu_items.append(f"• {course_name}")

        if not menu_items:
            return "Ingen meny idag"

        return "\n".join(menu_items)


async def get_api_client(session: aiohttp.ClientSession) -> MatildaPlatformAPI:
    """Get or create API client."""
    return MatildaPlatformAPI(session)
