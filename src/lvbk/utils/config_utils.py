"""
Configuration utilities for LVBK system.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dict[str, Any]: Loaded configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config or {}
        
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in config file {config_path}: {e}")


def get_config_value(
    config: Dict[str, Any],
    key: str,
    default: Any = None,
    required: bool = False
) -> Any:
    """
    Get configuration value with optional default.
    
    Args:
        config: Configuration dictionary
        key: Configuration key (supports dot notation)
        default: Default value if key not found
        required: Whether the key is required
        
    Returns:
        Any: Configuration value
        
    Raises:
        KeyError: If required key is not found
    """
    keys = key.split('.')
    value = config
    
    try:
        for k in keys:
            value = value[k]
        return value
        
    except (KeyError, TypeError):
        if required:
            raise KeyError(f"Required configuration key not found: {key}")
        return default


def get_env_config(
    key: str,
    default: Any = None,
    required: bool = False
) -> Any:
    """
    Get configuration value from environment variable.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        
    Returns:
        Any: Environment variable value
        
    Raises:
        KeyError: If required environment variable is not found
    """
    value = os.getenv(key)
    
    if value is None:
        if required:
            raise KeyError(f"Required environment variable not found: {key}")
        return default
    
    # Try to convert to appropriate type
    if isinstance(default, bool):
        return value.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(default, int):
        try:
            return int(value)
        except ValueError:
            return default
    elif isinstance(default, float):
        try:
            return float(value)
        except ValueError:
            return default
    
    return value


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple configuration dictionaries.
    
    Args:
        *configs: Configuration dictionaries to merge
        
    Returns:
        Dict[str, Any]: Merged configuration
    """
    merged = {}
    
    for config in configs:
        if config:
            merged.update(config)
    
    return merged
