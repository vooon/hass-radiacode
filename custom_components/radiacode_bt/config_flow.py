"""Adds config flow for RadiaCode 101 sensor component."""
from homeassistant import config_entries
from homeassistant.const import CONF_MAC, CONF_NAME
from radiacode.transports.bluetooth import Bluetooth as BTPeriph, DeviceNotFound
import voluptuous as vol

from .const import DOMAIN


class RadiacodeBtFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for radiacode_bt."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_device_presence(user_input[CONF_MAC])
            if valid:
                return self.async_create_entry(title=user_input[CONF_NAME],
                                               data=user_input)
            else:
                self._errors["base"] = "not_found"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_MAC): str
            }),
            errors=self._errors,
        )

    async def _test_device_presence(self, mac):
        """Return true if device exists."""
        try:
            BTPeriph(mac)
            return True
        except DeviceNotFound:
            pass
        except Exception:  # pylint: disable=broad-except
            pass
        return False
