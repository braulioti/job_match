"""
Config Manager
Manages configuration file operations
"""

import configparser
from pathlib import Path
from src.config.settings import Settings
from src.manager.base_manager import BaseManager


class ConfigManager(BaseManager):
    """Manager class for configuration file operations"""
    
    def __init__(self):
        """Initialize the config manager"""
        super().__init__()
        self.config_path = Settings.get_config_path()
        self.filename = str(self.config_path)
        self.config = configparser.ConfigParser()
        self._ensure_config_file()
        self._load_config()
    
    def _ensure_config_file(self):
        """Ensure config.ini file exists, create with default values if it doesn't"""
        if not self.config_path.exists():
            # Create default configuration
            self.config['Application'] = {
                'name': Settings.APP_NAME,
                'version': Settings.APP_VERSION
            }
            
            self.config['Database'] = {
                'name': Settings.DB_NAME,
                'path': str(Settings.get_db_path())
            }
            
            self.config['Window'] = {
                'width': str(Settings.WINDOW_WIDTH),
                'height': str(Settings.WINDOW_HEIGHT),
                'min_width': str(Settings.WINDOW_MIN_WIDTH),
                'min_height': str(Settings.WINDOW_MIN_HEIGHT)
            }
            
            self.config['Server'] = {
                'url': ''
            }
            
            # Save the default configuration
            try:
                self.config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as configfile:
                    self.config.write(configfile)
                print(f"Arquivo de configuração criado: {self.config_path}")
            except Exception as e:
                print(f"Erro ao criar arquivo de configuração: {e}")
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                self.config.read(self.config_path, encoding='utf-8')
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
    
    def get(self, section, key, fallback=None):
        """
        Get a configuration value
        
        Args:
            section: Configuration section name
            key: Configuration key name
            fallback: Default value if key doesn't exist
        
        Returns:
            str: Configuration value or fallback
        """
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def set(self, section, key, value):
        """
        Set a configuration value
        
        Args:
            section: Configuration section name
            key: Configuration key name
            value: Value to set
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
