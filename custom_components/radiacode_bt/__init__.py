"""
Custom integration to integrate RadiaCode 101 sensor component with Home Assistant.

For more details about this integration, please refer to
https://github.com/vooon/hass-radiacode
"""
import asyncio
import logging
import typing
from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from radiacode import DoseRateDB
from radiacode import RadiaCode
from radiacode import RareData

from .const import DOMAIN
from .const import PLATFORMS
from .const import STARTUP_MESSAGE

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    mac = entry.data.get(CONF_MAC)

    coordinator = RadiacodeBtDataUpdateCoordinator(hass, mac=mac)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        coordinator.platforms.append(platform)
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.add_update_listener(async_reload_entry)
    return True


@dataclass
class Data:
    dose_rate_db: typing.Optional[DoseRateDB] = None
    rare_data: typing.Optional[RareData] = None

    @classmethod
    def from_data_buf(cls, data_buf: typing.List[typing.Any]) -> "Data":
        dose_rate_db = None
        rare_data = None
        for msg in data_buf:
            if isinstance(msg, DoseRateDB):
                dose_rate_db = msg
            elif isinstance(msg, RareData):
                rare_data = msg

        return cls(dose_rate_db, rare_data)


class RadiacodeBtDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    mac: str = ""

    api: typing.Optional[RadiaCode] = None

    last_dose_rate_db: typing.Optional[DoseRateDB] = None
    last_rare_data: typing.Optional[RareData] = None
    last_fw_version: str = "unknown"
    last_serial_number: str = "RC-101-unknown"

    def __init__(
        self,
        hass: HomeAssistant,
        mac: str,
    ) -> None:
        """Initialize."""
        self.mac = mac
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.hass.async_add_executor_job(self._get_data)
        except Exception as exception:
            self.api = None
            _LOGGER.exception("Failed to get data_buf")
            raise UpdateFailed() from exception

    def _get_data(self) -> Data:
        if self.api is None:
            _LOGGER.info(f"Connecting to: {self.mac}")
            self.api = RadiaCode(bluetooth_mac=self.mac)
            self.last_fw_version = self.api.fw_version()
            _LOGGER.info(f"firmware: {self.last_fw_version}")
            # self.last_serial_number = self.api.serial_number()
            _LOGGER.info(f"serial number: {self.last_serial_number}")

        _LOGGER.info(f"Getting data from: {self.mac}")
        data = Data.from_data_buf(self.api.data_buf())
        if data.dose_rate_db:
            self.last_dose_rate_db = data.dose_rate_db
        if data.rare_data:
            self.last_rare_data = data.rare_data

        _LOGGER.info(f"got the data: {data}")
        return data


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
