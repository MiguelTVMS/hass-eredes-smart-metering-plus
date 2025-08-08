"""Webhook handling for E-Redes Smart Metering Plus integration."""

from __future__ import annotations

import logging

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

WEBHOOK_ID_KEY = "webhook_id"
SIGNAL_WEBHOOK_DATA = f"{DOMAIN}_webhook_data"


async def async_setup_webhook(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up the webhook for the config entry."""
    webhook_id = entry.data[WEBHOOK_ID_KEY]

    webhook.async_register(
        hass,
        DOMAIN,
        "E-Redes Smart Metering Plus",
        webhook_id,
        handle_webhook,
    )

    _LOGGER.info("Registered webhook with ID: %s", webhook_id)


async def async_unload_webhook(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unload the webhook for the config entry."""
    webhook_id = entry.data[WEBHOOK_ID_KEY]
    webhook.async_unregister(hass, webhook_id)
    _LOGGER.info("Unregistered webhook with ID: %s", webhook_id)


async def handle_webhook(hass: HomeAssistant, webhook_id: str, request) -> None:
    """Handle incoming webhook data."""
    try:
        # Parse the webhook data
        data = await request.json()
        _LOGGER.debug("Received webhook data: %s", data)

        # Send signal to update sensors
        async_dispatcher_send(
            hass,
            SIGNAL_WEBHOOK_DATA,
            {
                "webhook_id": webhook_id,
                "data": data,
            },
        )

    except Exception as err:
        _LOGGER.error("Error processing webhook data: %s", err)
        raise
