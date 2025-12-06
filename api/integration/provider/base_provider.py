"""
Base Provider
Base class for all provider classes
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Base class for all provider classes"""
    
    def __init__(self):
        """Initialize the base provider"""
        self._initialized = False
    
    @property
    def initialized(self):
        """Get the initialization status"""
        return self._initialized
    
    @initialized.setter
    def initialized(self, value):
        """Set the initialization status"""
        self._initialized = value
    
    @abstractmethod
    def initialize(self):
        """
        Initialize the provider
        Must be implemented by subclasses
        """
        pass
    
    def is_initialized(self):
        """
        Check if the provider is initialized
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized

