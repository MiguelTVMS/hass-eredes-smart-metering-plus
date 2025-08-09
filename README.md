# E-Redes Smart Metering Plus

A Home Assistant custom integration for E-Redes Smart Metering Plus service that provides webhook endpoints to receive smart meter data.

## Features

- **Webhook Integration**: Receives smart meter data via webhooks from E-Redes
- **Easy Configuration**: Simple setup through Home Assistant UI
- **Real-time Data**: Push-based updates for immediate data processing
- **Secure**: Uses Home Assistant's webhook authentication system

## Installation

### Manual Installation

1. Download the latest release from [GitHub releases](https://github.com/MiguelTVMS/hass-eredes-smart-metering-plus/releases)
2. Extract the contents
3. Copy the `custom_components/eredes_smart_metering_plus` directory to your Home Assistant's `custom_components` directory
4. Restart Home Assistant
5. Go to **Configuration** > **Integrations** > **Add Integration**
6. Search for "E-Redes Smart Metering Plus" and add it

### HACS Installation

1. Add this repository to HACS as a custom repository
2. Install "E-Redes Smart Metering Plus" from HACS
3. Restart Home Assistant
4. Add the integration through the Home Assistant UI

## Configuration

1. In Home Assistant, go to **Configuration** > **Integrations**
2. Click **Add Integration** and search for "E-Redes Smart Metering Plus"
3. Follow the configuration flow
4. The integration will provide you with a webhook URL
5. Configure this webhook URL in your E-Redes account

## Webhook URL

After configuration, you can view your webhook URL in:
- **Configuration** > **Integrations** > **E-Redes Smart Metering Plus** > **Configure**

The webhook URL will be in the format:
```
https://your-home-assistant-url/api/webhook/your-webhook-id
```

## Development

### Project Structure

```
custom_components/eredes_smart_metering_plus/  # Main integration code
├── __init__.py
├── config_flow.py
├── const.py
├── icons.json
├── manifest.json
├── quality_scale.yaml
├── sensor.py
├── strings.json
├── translations/
└── webhook.py

tests/custom_components/eredes_smart_metering_plus/  # Test files
├── conftest.py
├── test_config_flow.py
├── test_integration.py
└── test_webhook_data.py
```

### Running Tests

```bash
python -m pytest tests/custom_components/eredes_smart_metering_plus/ -v
```

## Support

For issues, feature requests, or questions:
- [GitHub Issues](https://github.com/MiguelTVMS/hass-eredes-smart-metering-plus/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
