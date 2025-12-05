"""
Base Manager
Base class for all manager classes
"""

from abc import ABC


class BaseManager(ABC):
    """Base class for all manager classes"""
    
    def __init__(self):
        """Initialize the base manager"""
        self._initialized = False
        self._filename = None
    
    @property
    def filename(self):
        """Get the filename"""
        return self._filename
    
    @filename.setter
    def filename(self, value):
        """Set the filename"""
        self._filename = value
