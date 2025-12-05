"""
Server Integration
Handles server integration operations
"""

from typing import Optional, Dict, Any
import requests
from src.interfaces.server import ServerInterface


class ServerIntegration:
    """Integration class for server operations"""
    
    def __init__(self):
        """Initialize the server integration"""
        self._server: Optional[ServerInterface] = None
    
    @property
    def server(self) -> Optional[ServerInterface]:
        """Get the current server"""
        return self._server
    
    @server.setter
    def server(self, value: ServerInterface):
        """Set the current server"""
        self._server = value
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check the health of the API server
        
        Returns:
            Dict containing:
                - success (bool): Whether the request was successful
                - status_code (int): HTTP status code
                - data (dict): Response data if successful, None otherwise
                - error (str): Error message if failed, None otherwise
        
        Raises:
            ValueError: If no server is configured
        """
        if not self._server:
            raise ValueError("No server configured. Set a server before checking health.")
        
        try:
            # Construct the health endpoint URL
            health_url = f"{self._server['url'].rstrip('/')}/health"
            
            # Make GET request to health endpoint
            response = requests.get(health_url, timeout=5)
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'data': response.json() if response.status_code == 200 else None,
                'error': None if response.status_code == 200 else f"HTTP {response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'status_code': None,
                'data': None,
                'error': str(e)
            }
