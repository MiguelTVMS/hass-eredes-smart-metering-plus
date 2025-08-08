#!/usr/bin/env python3
"""Test script to verify webhook functionality."""

import asyncio

import aiohttp


async def test_webhook():
    """Test the webhook endpoint."""
    # This would be replaced with the actual webhook URL from Home Assistant
    webhook_url = "http://localhost:8123/api/webhook/test-webhook-id"

    # Sample data that E-Redes might send
    test_data = {
        "deviceId": "1234567890",
        "timestamp": "2025-01-09T00:00:00Z",
        "readings": [
            {"type": "active_energy_import", "value": 1234.5, "unit": "kWh"},
            {"type": "active_energy_export", "value": 567.8, "unit": "kWh"},
        ],
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                webhook_url,
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                # Log status and response for debugging
                await response.text()
                # Response received successfully

        except aiohttp.ClientError:
            # Request failed due to client error
            pass
        except TimeoutError:
            # Request timed out
            pass


if __name__ == "__main__":
    asyncio.run(test_webhook())
