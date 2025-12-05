"""
Application Settings
"""

import os
import sys
from pathlib import Path


class Settings:
    """Application settings"""
    
    # Application info
    APP_NAME = "Job Match"
    APP_VERSION = "0.1.0"
    
    # Database settings
    DB_NAME = "projects.job.match"  # Nome padrão do banco de dados
    
    # Paths
    # Determina o diretório base: pasta do executável ou pasta do script
    if getattr(sys, 'frozen', False):
        # Executável compilado (PyInstaller)
        BASE_DIR = Path(sys.executable).parent
    else:
        # Modo desenvolvimento
        BASE_DIR = Path(__file__).parent.parent.parent
    
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Database path
    @classmethod
    def get_db_path(cls):
        """Get the full path to the database file"""
        return cls.BASE_DIR / f"{cls.DB_NAME}"
    
    # Images path
    @classmethod
    def get_favicon_path(cls):
        """Get the full path to the favicon file"""
        return cls.BASE_DIR / "images" / "favicon.ico"
    
    @classmethod
    def get_logo_path(cls):
        """Get the full path to the logo file"""
        return cls.BASE_DIR / "images" / "job_match_logo.png"
    
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

