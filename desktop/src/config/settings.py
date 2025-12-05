"""
Application Settings
"""

import os
import sys
from pathlib import Path
import configparser


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
    def get_config_path(cls):
        """Get the full path to the config.ini file"""
        return cls.BASE_DIR / "config.ini"
    
    @classmethod
    def get_servers_path(cls):
        """Get the full path to the servers file"""
        return cls.BASE_DIR / "servers"
    
    @classmethod
    def initialize_directories(cls):
        """Initialize required directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def initialize_config_file(cls):
        """Initialize config.ini file if it doesn't exist"""
        config_path = cls.get_config_path()
        
        if not config_path.exists():
            config = configparser.ConfigParser()
            
            # Application section
            config['Application'] = {
                'name': cls.APP_NAME,
                'version': cls.APP_VERSION
            }
            
            # Database section
            config['Database'] = {
                'name': cls.DB_NAME,
                'path': str(cls.get_db_path())
            }
            
            # Window section
            config['Window'] = {
                'width': str(cls.WINDOW_WIDTH),
                'height': str(cls.WINDOW_HEIGHT),
                'min_width': str(cls.WINDOW_MIN_WIDTH),
                'min_height': str(cls.WINDOW_MIN_HEIGHT)
            }
            
            # Write config file
            try:
                with open(config_path, 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
                print(f"Arquivo de configuração criado: {config_path}")
            except Exception as e:
                print(f"Erro ao criar arquivo de configuração: {e}")

