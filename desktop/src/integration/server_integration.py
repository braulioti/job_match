"""
Server Integration
Handles server integration operations
"""

from typing import Optional
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
