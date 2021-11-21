"""Constants for RadiaCode 101 sensor component."""
from typing import Final

# Base component constants
NAME = "RadiaCode 101"
DOMAIN = "radiacode_bt"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = ""
ISSUE_URL = "https://github.com/vooon/hass-radiacode/issues"

MANUFACTURER = "https://scan-electronics.com/"

# Icons
ICON: Final = "mdi:radioactive"

# Device classes
SENSOR_DEVICE_CLASS: Final = "radioactivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [
    SENSOR,
]

# Units
MICROSIEVERT_HOUR: Final = "μSv/h"
COUNT_PER_SECOND: Final = "CPS"

# Config entries
CONF_METHOD: Final = "method"
CONF_METHOD_SCAN: Final = "Scan"
CONF_METHOD_MANUAL: Final = "Manual"

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
