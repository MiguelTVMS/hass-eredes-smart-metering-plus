"""Test the E-Redes Smart Metering Plus config flow."""

from unittest.mock import AsyncMock

from homeassistant import config_entries
from homeassistant.components.eredes_smart_metering_plus.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None  # No errors on initial form
    assert result["step_id"] == "user"

    # Check that webhook_url is in the form data schema
    assert "webhook_url" in result["data_schema"].schema

    # Complete the flow by submitting the form with webhook_url
    # (since it's readonly, the value doesn't matter)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"webhook_url": "http://example.com/webhook"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "E-Redes Smart Metering Plus"
    assert "webhook_id" in result["data"]
    assert len(mock_setup_entry.mock_calls) == 1


async def test_options_flow_webhook_url_display(hass: HomeAssistant) -> None:
    """Test that options flow displays the webhook URL correctly."""
    # Create a mock config entry with webhook data
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "webhook_id": "test-webhook-id-123",
            "webhook_url": "https://example.com/api/webhook/test-webhook-id-123",
        },
        entry_id="test-entry-id",
        title="E-Redes Smart Metering Plus",
    )
    config_entry.add_to_hass(hass)

    # Start the options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    # Check that the webhook URL is displayed in the form
    assert "webhook_url" in result["data_schema"].schema

    # Check that the webhook URL from config entry is available in placeholders
    assert (
        result["description_placeholders"]["webhook_url"]
        == "https://example.com/api/webhook/test-webhook-id-123"
    )

    # Complete the options flow
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"webhook_url": "https://example.com/api/webhook/test-webhook-id-123"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == ""
    assert result["data"] == {}
