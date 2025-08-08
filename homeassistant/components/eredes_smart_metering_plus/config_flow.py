"""Config flow for the E-Redes Smart Metering Plus integration."""

from __future__ import annotations

import logging
from typing import Any
import uuid

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Data schema for webhook setup - just needs a name
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="E-Redes Smart Meter"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to set up the integration.

    For webhook integrations, we don't need to validate external connections.
    """
    # Generate a unique webhook ID
    webhook_id = str(uuid.uuid4())

    # Return info that you want to store in the config entry
    return {
        "title": data["name"],
        "webhook_id": webhook_id,
    }


class EredesSmartMeteringPlusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for E-Redes Smart Metering Plus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                # Set unique ID to prevent duplicates
                await self.async_set_unique_id(info["webhook_id"])
                self._abort_if_unique_id_configured()

                # Store both the name and webhook_id
                config_data = {
                    "name": user_input["name"],
                    "webhook_id": info["webhook_id"],
                }

                return self.async_create_entry(title=info["title"], data=config_data)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
