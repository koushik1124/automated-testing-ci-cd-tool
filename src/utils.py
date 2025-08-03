import json
import logging
import os
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing configuration data
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file contains invalid JSON
    """
    if not os.path.exists(config_path):
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from: {config_path}")
        return config
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise

def get_config_value(section: str, key: str, default: Any = None, config_path: str = "config.json") -> Any:
    """Get a configuration value with nested keys.
    
    Args:
        section: The section of the config to look in
        key: The key to retrieve
        default: Default value if key not found
        config_path: Path to the configuration file
        
    Returns:
        The configuration value or default
    """
    try:
        config = load_config(config_path)
        return config.get(section, {}).get(key, default)
    except Exception:
        return default

def ensure_directory_exists(directory_path: str) -> bool:
    """Ensure a directory exists, create it if necessary.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    logger.info(f"Ensuring directory exists: {directory_path}")
    
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Directory created: {directory_path}")
        else:
            logger.info(f"Directory already exists: {directory_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating directory: {e}")
        return False

def save_json(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to the output file
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    logger.info(f"Saving JSON data to: {file_path}")
    
    try:
        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data successfully saved to: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving JSON data: {e}")
        return False

def get_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable with an optional default value.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if the variable is not set
        
    Returns:
        Value of the environment variable or default
    """
    logger.debug(f"Getting environment variable: {var_name}")
    
    value = os.environ.get(var_name, default)
    
    if value is None:
        logger.warning(f"Environment variable not set and no default provided: {var_name}")
    
    return value