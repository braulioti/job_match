"""
Helper utility functions
"""

from datetime import datetime
from typing import Dict, Any


def format_response(data: Any, message: str = None, status_code: int = 200) -> Dict:
    """Format API response"""
    response = {
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    
    if message:
        response['message'] = message
    
    return response


def validate_required_fields(data: Dict, required_fields: list) -> tuple:
    """
    Validate required fields in request data
    
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, missing_fields
    
    return True, []
