import json
import requests
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def file_automation(file_path: str) -> Dict[str, Any]:
    """Automate file operations.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Dict containing operation results
    """
    logger.info(f"Starting file automation for: {file_path}")
    
    result = {
        "success": False,
        "message": "",
        "data": None
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result["message"] = f"File not found: {file_path}"
            return result
        
        # Read file content
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Try to parse as JSON
        try:
            data = json.loads(file_content)
            result["data"] = data
            result["message"] = "File successfully processed as JSON"
            result["success"] = True
        except json.JSONDecodeError:
            result["message"] = "File content is not valid JSON"
            result["data"] = file_content
        
        logger.info(f"File automation completed for: {file_path}")
        return result
    
    except Exception as e:
        logger.error(f"Error in file automation: {e}")
        result["message"] = f"Error processing file: {str(e)}"
        return result

def api_automation(url: str, method: str = "GET", 
                  headers: Optional[Dict[str, str]] = None, 
                  data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Automate API operations.
    
    Args:
        url: API endpoint URL
        method: HTTP method (GET, POST, etc.)
        headers: HTTP headers
        data: Request body data
        
    Returns:
        Dict containing operation results
    """
    logger.info(f"Starting API automation for: {url} with method: {method}")
    
    result = {
        "success": False,
        "message": "",
        "data": None,
        "status_code": None
    }
    
    try:
        # Prepare request
        request_kwargs = {
            "url": url,
            "method": method.upper(),
            "headers": headers or {}
        }
        
        if method.upper() in ["POST", "PUT", "PATCH"] and data:
            request_kwargs["json"] = data
        
        # Make the request
        response = requests.request(**request_kwargs)
        result["status_code"] = response.status_code
        
        # Check if request was successful
        if response.status_code >= 200 and response.status_code < 300:
            try:
                result["data"] = response.json()
                result["message"] = "API request successful"
                result["success"] = True
            except json.JSONDecodeError:
                result["data"] = response.text
                result["message"] = "API request successful but response is not JSON"
                result["success"] = True
        else:
            result["message"] = f"API request failed with status code: {response.status_code}"
            try:
                result["data"] = response.json()
            except json.JSONDecodeError:
                result["data"] = response.text
        
        logger.info(f"API automation completed for: {url}")
        return result
    
    except Exception as e:
        logger.error(f"Error in API automation: {e}")
        result["message"] = f"Error making API request: {str(e)}"
        return result