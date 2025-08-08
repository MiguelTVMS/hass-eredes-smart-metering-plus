"""Config flow for the E-Redes Smart Metering Plus integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def create_webhook_info_schema(webhook_url: str) -> vol.Schema:
    """Create schema showing webhook URL as readonly field."""
    return vol.Schema(
        {
            vol.Required(
                "webhook_url",
                default=webhook_url,
                description={"suggested_value": webhook_url},
            ): str,
        }
    )


class EredesSmartMeteringPlusConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for E-Redes Smart Metering Plus."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._webhook_id: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step - show webhook info directly."""
        # Generate webhook ID only once
        if self._webhook_id is None:
            self._webhook_id = webhook.async_generate_id()
            # Set unique ID to prevent duplicates
            await self.async_set_unique_id(self._webhook_id)
            self._abort_if_unique_id_configured()

        if user_input is not None:
            # User confirmed, create the entry
            return self.async_create_entry(
                title="E-Redes Smart Metering Plus",
                data={
                    "webhook_id": self._webhook_id,
                },
            )

        # Generate the preview URL for display (this will be recreated during setup)
        preview_url = webhook.async_generate_url(self.hass, self._webhook_id)

        # Show webhook information form
        return self.async_show_form(
            step_id="user",
            data_schema=create_webhook_info_schema(preview_url),
            description_placeholders={"webhook_url": preview_url},
        )
