"""
Data Models
SQLAlchemy models for the API

This module imports all models to ensure they are registered with SQLAlchemy.
"""

# Import all models to ensure they are registered
from api.models.base_model import BaseModel
from api.models.file import File
from api.models.user import User

__all__ = ['BaseModel', 'File', 'User']
