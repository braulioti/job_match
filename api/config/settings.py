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
    
    # Database - PostgreSQL
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'job_match')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Legacy SQLite path (for backward compatibility)
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or str(Path(__file__).parent.parent.parent / 'desktop' / 'projects.job.match')
    
    # API
    API_VERSION = 'v1'
    API_PREFIX = '/api/v1'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Prompt Configuration
    PROMPT_JOB_ANALYS = os.environ.get('PROMPT_JOB_ANALYS', './prompts/job_vacancy_analysis.txt')


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


