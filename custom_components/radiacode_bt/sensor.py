"""Sensor platform for RadiaCode 101 sensor component."""
from homeassistant.const import CONF_NAME

from .const import COUNT_PER_SECOND
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import MICROSIEVERT_HOUR
from .const import SENSOR_DEVICE_CLASS
from .entity import RadiacodeBtEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            RadiacodeBtSensorDoseRate(coordinator, entry),
            RadiacodeBtSensorCountRate(coordinator, entry),
        ]
    )


class RadiacodeBtSensorDoseRate(RadiacodeBtEntity):
    """radiacode_bt Sensor Dose Rate class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)
        return f"{name} rate"

    @property
    def state(self):
        """Return the state of the sensor."""
        d = self.coordinator.data.dose_rate_db or self.coordinator.last_dose_rate_db
        return d.dose_rate

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return MICROSIEVERT_HOUR

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return SENSOR_DEVICE_CLASS


class RadiacodeBtSensorCountRate(RadiacodeBtEntity):
    """radiacode_bt Sensor Count Rate class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)
        return f"{name} count"

    @property
    def state(self):
        """Return the state of the sensor."""
        d = self.coordinator.data.dose_rate_db or self.coordinator.last_dose_rate_db
        return d.count_rate

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return COUNT_PER_SECOND

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return SENSOR_DEVICE_CLASS
