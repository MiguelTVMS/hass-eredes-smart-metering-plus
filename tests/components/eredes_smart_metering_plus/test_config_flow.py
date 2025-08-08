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
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Test E-Redes Integration"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Test E-Redes Integration"
    assert "name" in result["data"]
    assert "webhook_id" in result["data"]
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_empty_name(
    hass: HomeAssistant, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle empty name."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": ""},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"name": "invalid_name"}

    # Recovery test - provide valid name
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Valid Name"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Valid Name"
    assert len(mock_setup_entry.mock_calls) == 1
