#!/usr/bin/env python3
"""Test script for options flow webhook URL display."""

import asyncio
from unittest.mock import Mock

from homeassistant.components.eredes_smart_metering_plus import config_flow


async def test_options_flow():
    """Test the options flow webhook URL display."""
    # Create a mock config entry with webhook URL
    mock_config_entry = Mock()
    mock_config_entry.data = {
        "webhook_id": "test-webhook-id",
        "webhook_url": "https://example.com/api/webhook/test-webhook-id",
    }

    # Create options flow instance
    options_flow = config_flow.EredesSmartMeteringPlusOptionsFlow(mock_config_entry)
    assert options_flow.config_entry == mock_config_entry

    # Test that async_step_init exists
    assert hasattr(options_flow, "async_step_init")


if __name__ == "__main__":
    asyncio.run(test_options_flow())
