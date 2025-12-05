"""
Server Interface
Defines the structure for server objects
"""

from typing import TypedDict


class ServerInterface(TypedDict):
    """
    Interface for server structure
    
    Attributes:
        name: Server name
        url: Server URL
        default: Whether this is the default server
    """
    name: str
    url: str
    default: bool
