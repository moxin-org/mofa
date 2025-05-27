"""Configuration loading utilities for the Euterpe library.

This module provides functions to load configuration from various sources.
"""

import os
from pathlib import Path
from typing import Optional

from .models import EuterpeConfig


def load_config(config_path: Optional[str] = None) -> EuterpeConfig:
    """Load configuration from environment variables and optional config file.
    
    Args:
        config_path: Optional path to a configuration file. If not provided,
            configuration will be loaded solely from environment variables.
            
    Returns:
        EuterpeConfig: Configuration object with API keys and settings.
    """
    # For now, simply create a config from environment variables
    # In a future implementation, this could read from YAML/JSON files
    return EuterpeConfig()
