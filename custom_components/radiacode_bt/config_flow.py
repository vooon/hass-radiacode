"""Adds config flow for RadiaCode 101 sensor component."""
import logging

import voluptuous as vol
from bluepy.btle import BTLEDisconnectError
from bluepy.btle import BTLEManagementError
from homeassistant import config_entries
from homeassistant.const import CONF_MAC
from homeassistant.const import CONF_NAME
from homeassistant.helpers import device_registry
from radiacode.transports.bluetooth import Bluetooth as BTPeriph

from .const import CONF_METHOD
from .const import CONF_METHOD_MANUAL
from .const import CONF_METHOD_SCAN
from .const import DOMAIN
from .helper import discover_devices

_logger = logging.getLogger(__name__)


class RadiacodeBtFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for radiacode_bt."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self.devices = []

    @property
    def data_schema(self):
        return vol.Schema(
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_MAC): str,
            }
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is None:
            schema = vol.Schema(
                {
                    vol.Required(CONF_METHOD): vol.In(
                        (CONF_METHOD_SCAN, CONF_METHOD_MANUAL)
                    )
                }
            )
            return self.async_show_form(step_id="user", data_schema=schema)

        method = user_input[CONF_METHOD]
        _logger.debug(f"selected method: {method}")
        if method == CONF_METHOD_SCAN:
            return await self.async_step_scan()
        else:
            self.devices = []
            return await self.async_step_device()

    async def async_step_scan(self, user_input=None):
        """Handle discovery by scanning."""
        errors = {}

        if user_input is None:
            return self.async_show_form(step_id="scan")

        _logger.debug("Starting a scan for RadiaCode devices...")
        try:
            devices = await self.hass.async_add_executor_job(discover_devices)
        except BTLEDisconnectError:
            _logger.exception("BLE Connection error")
            errors["base"] = "btle_disconnection"
            return self.async_show_form(step_id="scan", errors=errors)
        except BTLEManagementError:
            _logger.exception("BLE Management error")
            errors["base"] = "btle_management"
            return self.async_show_form(step_id="scan", errors=errors)

        if not devices:
            return self.async_abort(reason="not_found")

        self.devices = devices
        return await self.async_step_device()

    async def async_step_device(self, user_input=None):
        """Handle setting up a device"""

        if not user_input:
            schema_mac = str
            if self.devices:
                schema_mac = vol.In(self.devices)
            schema = vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_MAC): schema_mac,
                }
            )
            return self.async_show_form(step_id="device", data_schema=schema)

        mac = user_input[CONF_MAC] = user_input[CONF_MAC].strip()
        unique_id = device_registry.format_mac(mac)
        _logger.info(f"Setting up RadiaCode MAC: {mac}, unique_id: {unique_id}")

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        try:
            BTPeriph(mac)
        except Exception:
            _logger.exception("Failed to connect to the device.")
            return self.async_show_form(step_id="device", errors={"base": "exception"})

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
