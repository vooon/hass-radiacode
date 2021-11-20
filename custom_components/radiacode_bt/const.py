"""Constants for RadiaCode 101 sensor component."""
import typing

# Base component constants
NAME = "RadiaCode 101"
DOMAIN = "radiacode_bt"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = ""
ISSUE_URL = "https://github.com/vooon/hass-radiacode/issues"

MANUFACTURER = "https://scan-electronics.com/"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [
    SENSOR,
]

# Config entries
CONF_METHOD: typing.Final = "method"
CONF_METHOD_SCAN = "Scan"
CONF_METHOD_MANUAL = "Manual"

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
