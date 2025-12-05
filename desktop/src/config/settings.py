"""
Application Settings
"""

import os
from pathlib import Path


class Settings:
    """Application settings"""
    
    # Application info
    APP_NAME = "Job Match"
    APP_VERSION = "0.1.0"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Window settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_MIN_WIDTH = 600
    WINDOW_MIN_HEIGHT = 400
    
    @classmethod
    def initialize_directories(cls):
        """Initialize required directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

