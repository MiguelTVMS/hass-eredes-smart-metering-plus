"""Test the E-Redes Smart Metering Plus config flow."""

from unittest.mock import AsyncMock

from homeassistant import config_entries
from homeassistant.components.eredes_smart_metering_plus.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


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
