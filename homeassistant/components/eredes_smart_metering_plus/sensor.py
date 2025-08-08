"""Sensor platform for E-Redes Smart Metering Plus integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EredesSmartMeteringPlusConfigEntry
from .webhook import SIGNAL_WEBHOOK_DATA


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EredesSmartMeteringPlusConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up E-Redes Smart Metering Plus sensor based on a config entry."""
    # Get the configuration data from the config entry
    config_data = entry.runtime_data

    # Add sensors
    async_add_entities(
        [
            EredesSmartMeterSensor(hass, config_data, "energy_consumption"),
            EredesSmartMeterSensor(hass, config_data, "power"),
        ]
    )


class EredesSmartMeterSensor(SensorEntity):
    """Representation of an E-Redes Smart Meter sensor."""

    _attr_has_entity_name = True

    def __init__(
        self, hass: HomeAssistant, config_data: dict[str, str], sensor_type: str
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._config_data = config_data
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{config_data['webhook_id']}_{sensor_type}"
        self._attr_name = sensor_type.replace("_", " ").title()

        # Initialize with None value - will be updated via webhook
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Subscribe to webhook data updates."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_WEBHOOK_DATA,
                self._handle_webhook_data,
            )
        )

    @callback
    def _handle_webhook_data(self, webhook_data: dict) -> None:
        """Handle incoming webhook data."""
        if webhook_data["webhook_id"] != self._config_data["webhook_id"]:
            return

        data = webhook_data["data"]

        # Extract the relevant data for this sensor type
        if self._sensor_type == "energy_consumption" and "energy" in data:
            self._attr_native_value = data["energy"]
        elif self._sensor_type == "power" and "power" in data:
            self._attr_native_value = data["power"]

        # Update the entity state
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the sensor.

        For webhook integrations, sensors are typically updated
        when webhook data is received, not through periodic polling.
        This method can be left empty or used for fallback logic.
        """
        # Webhook integrations don't typically need periodic updates
