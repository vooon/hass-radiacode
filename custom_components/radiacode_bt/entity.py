"""RadiacodeBtEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .const import MANUFACTURER
from .const import NAME


class RadiacodeBtEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        fw_version = self.coordinator.last_fw_version
        serial_number = self.coordinator.last_serial_number

        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": serial_number,
            "manufacturer": MANUFACTURER,
            "sw_version": fw_version,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        battery_level = None
        if self.coordinator.last_rare_data:
            battery_level = float(self.coordinator.last_rare_data.charge_level)

        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
            "battery_level": battery_level,
        }
