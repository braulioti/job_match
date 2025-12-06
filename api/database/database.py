"""
Database Configuration
SQLAlchemy database setup and session management
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Create SQLAlchemy instance
db = SQLAlchemy()


def init_db(app: Flask):
    """
    Initialize database with Flask application
    
    Args:
        app: Flask application instance
    
    Note: This function is kept for backward compatibility.
    The actual initialization with migrations is handled in app.py
    """
    db.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from api.models import models  # noqa: F401


def get_db_session():
    """
    Get database session
    
    Returns:
        SQLAlchemy session
    """
    return db.session

