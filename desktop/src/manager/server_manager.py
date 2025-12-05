"""
Server Manager
Manages server-related operations
"""

from pathlib import Path
from typing import List, Optional
from src.manager.base_manager import BaseManager
from src.config.settings import Settings
from src.interfaces.server import ServerInterface


class ServerManager(BaseManager):
    """Manager class for server operations"""
    
    def __init__(self):
        """Initialize the server manager"""
        super().__init__()
        self.servers_path = Settings.get_servers_path()
        self.filename = str(self.servers_path)
        self._servers: List[ServerInterface] = []
        self._load_servers()
    
    def _load_servers(self):
        """Load servers from file and parse into structured format"""
        self._servers = []
        
        if self.servers_path.exists():
            try:
                with open(self.servers_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        
                        parts = [part.strip() for part in line.split(';')]

                        if len(parts) >= 2:
                            name = parts[0]
                            url = parts[1]

                            is_default = False
                            if len(parts) >= 3:
                                is_default = parts[2].lower() == 'default'
                            
                            server: ServerInterface = {
                                'name': name,
                                'url': url,
                                'default': is_default
                            }
                            
                            self._servers.append(server)
            except Exception as e:
                print(f"Erro ao carregar servidores: {e}")
                self._servers = []
        else:
            self._servers = []
    
    @property
    def servers(self) -> List[ServerInterface]:
        """Get the list of servers"""
        return self._servers
    
    def get_server_by_url(self, url: str) -> Optional[ServerInterface]:
        """
        Get a server by its URL
        
        Args:
            url: Server URL to search for
        
        Returns:
            ServerInterface: Server matching the URL, or None if not found
        """
        for server in self._servers:
            if server['url'] == url:
                return server
        return None
    
    def get_default_server(self) -> Optional[ServerInterface]:
        """
        Get the default server
        
        Returns:
            ServerInterface: Default server, or first server if no default, or None if no servers
        """
        # First, try to find a server marked as default
        for server in self._servers:
            if server.get('default', False):
                return server
        
        # If no default, return the first server
        if self._servers:
            return self._servers[0]
        
        return None
