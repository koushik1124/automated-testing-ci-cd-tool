import json
import logging
import argparse
import os
from typing import Dict, Any, Union
from venv import logger
from src.utils import load_config, get_config_value

def validate_input(data: Dict[str, Any]) -> bool:
    """Validate input data.
    
    Args:
        data: Input data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    required_fields = ["name", "value"]
    for field in required_fields:
        if field not in data:
            return False
    
    if not isinstance(data["name"], str) or not data["name"]:
        return False
    
    if not isinstance(data["value"], (int, float)) or data["value"] < 0:
        return False
    
    return True

def process_data(data: Dict[str, Any], config_path: str = "config.json") -> Dict[str, Any]:
    """Process input data.
    
    Args:
        data: Input data to process
        config_path: Path to the configuration file
        
    Returns:
        Dict containing processed data
        
    Raises:
        ValueError: If input data is invalid
    """
    if not validate_input(data):
        raise ValueError("Invalid input data")
    
    logger.info(f"Processing data: {data}")
    
    # Get processing parameters from config
    multiplier = get_config_value("processing", "default_multiplier", 2, config_path)
    
    # Example processing: multiply the value by the configured multiplier
    processed_value = data["value"] * multiplier
    
    result = {
        "status": "success",
        "original_value": data["value"],
        "processed_value": processed_value,
        "name": data["name"]
    }
    
    logger.info(f"Processing complete: {result}")
    return result

def process_file(file_path: str, config_path: str = "config.json") -> Dict[str, Any]:
    """Process data from a file.
    
    Args:
        file_path: Path to the file to process
        config_path: Path to the configuration file
        
    Returns:
        Dict containing processed data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
        ValueError: If file data is invalid
    """
    logger.info(f"Processing file: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file: {file_path}, error: {e}")
        raise
    
    return process_data(data, config_path)

def process_api_response(response_data: Dict[str, Any], config_path: str = "config.json") -> Dict[str, Any]:
    """Process data from an API response.
    
    Args:
        response_data: API response data
        config_path: Path to the configuration file
        
    Returns:
        Dict containing processed data
    """
    logger.info("Processing API response")
    
    # Extract relevant data from the response
    extracted_data = {
        "name": response_data.get("title", "Unknown"),
        "value": response_data.get("id", 0)
    }
    
    try:
        result = process_data(extracted_data, config_path)
        result["status"] = "processed"
        return result
    except ValueError as e:
        logger.error(f"Error processing API response: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Automated Testing CI/CD Tool")
    parser.add_argument("--config", type=str, default="config.json", 
                        help="Path to configuration file")
    parser.add_argument("--input", type=str, 
                        help="Path to input file to process")
    parser.add_argument("--api", type=str,
                        help="API endpoint to query")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return 1
    
    # Configure logging based on config and command line
    log_level = logging.DEBUG if args.verbose else getattr(
        logging, 
        config.get("logging", {}).get("level", "INFO")
    )
    log_format = config.get("logging", {}).get("format", 
                     "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Set up logging
    logging.basicConfig(
        level=log_level,
        format=log_format
    )
    
    # Set up file logging if configured
    log_file = config.get("logging", {}).get("file")
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting automated testing CI/CD tool")
    
    try:
        # Process file if specified
        if args.input:
            logger.info(f"Processing file: {args.input}")
            result = process_file(args.input, args.config)
            print(f"Result: {result}")
        
        # Process API if specified
        elif args.api:
            logger.info(f"Querying API: {args.api}")
            from .automation import api_automation
            response = api_automation(args.api)
            if response["success"]:
                processed = process_api_response(response["data"], args.config)
                print(f"Processed result: {processed}")
            else:
                print(f"API request failed: {response['message']}")
        
        # If no specific action, run sample processing
        else:
            # Use sample data from config or default
            sample_data = config.get("test_data", {}).get("valid_sample", 
                          {"name": "Sample", "value": 10})
            result = process_data(sample_data, args.config)
            print(f"Sample processing result: {result}")
    
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
