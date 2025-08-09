#!/usr/bin/env python3
"""Test script for E-Redes Smart Metering Plus custom component."""

import logging
from pathlib import Path
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Add the custom component to Python path
custom_components_path = Path(__file__).parent / "custom_components"
sys.path.insert(0, str(custom_components_path))

try:
    from eredes_smart_metering_plus import const

    logger.info("✅ Custom component loaded successfully!")
    logger.info("✅ Domain: %s", const.DOMAIN)
    logger.info(
        "✅ Integration files found in: %s",
        custom_components_path / "eredes_smart_metering_plus",
    )

    # Check all required files exist
    required_files = [
        "__init__.py",
        "config_flow.py",
        "const.py",
        "manifest.json",
        "strings.json",
    ]

    integration_path = custom_components_path / "eredes_smart_metering_plus"

    for file in required_files:
        file_path = integration_path / file
        if file_path.exists():
            logger.info("✅ %s - Found", file)
        else:
            logger.error("❌ %s - Missing", file)

except ImportError as e:
    logger.error("❌ Failed to load custom component: %s", e)
    sys.exit(1)
except (OSError, RuntimeError) as e:
    logger.error("❌ Error: %s", e)
    sys.exit(1)
