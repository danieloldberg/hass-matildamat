"""Matilda Platform integration for Home Assistant."""
import logging
from typing import Final

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "matilda_platform"
PLATFORMS: Final = ["sensor"]

# API Configuration
MATILDA_API_BASE: Final = "https://menu.matildaplatform.com/api"
MATILDA_DISTRIBUTORS_URL: Final = f"{MATILDA_API_BASE}/distributors"
MATILDA_MENU_URL: Final = f"{MATILDA_API_BASE}/menu"

# Config keys
CONF_DISTRIBUTOR_ID: Final = "distributor_id"
CONF_DISTRIBUTOR_NAME: Final = "distributor_name"

# Sensor configuration
SCAN_INTERVAL_HOURS: Final = 1  # Check menu every hour
