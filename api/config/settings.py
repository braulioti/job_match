"""
Application Configuration
"""

import os
from pathlib import Path


class Config:
    """Base configuration"""
    
    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or str(Path(__file__).parent.parent.parent / 'desktop' / 'projects.job.match')
    
    # API
    API_VERSION = 'v1'
    API_PREFIX = '/api/v1'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
