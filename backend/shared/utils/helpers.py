"""
Common helper functions
"""
from typing import Any, Dict
import json


def json_loads_safe(data: str, default: Any = None) -> Any:
    """
    Safely parse JSON string, return default if parsing fails
    
    Args:
        data: JSON string to parse
        default: Default value to return if parsing fails
        
    Returns:
        Parsed JSON object or default value
    """
    if not data:
        return default
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def json_dumps_safe(data: Any, default: str = "[]") -> str:
    """
    Safely convert object to JSON string
    
    Args:
        data: Object to serialize
        default: Default JSON string if serialization fails
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return default


def format_error_response(message: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Format error response consistently
    
    Args:
        message: Error message
        details: Additional error details
        
    Returns:
        Formatted error dictionary
    """
    response = {"error": message}
    if details:
        response["details"] = details
    return response
