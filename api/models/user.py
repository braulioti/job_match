"""
User Model
Model for storing user information
"""

from api.models.base_model import BaseModel
from api.database.database import db


class User(BaseModel):
    """User model for storing user information"""
    __tablename__ = 'user'
    
    email = db.Column(db.String(255), nullable=False, unique=True, comment='User email address')
    password = db.Column(db.String(255), nullable=False, comment='Hashed password')
    hash = db.Column(db.String(36), nullable=True, unique=True, comment='UUID v4 hash for authentication')
    last_login = db.Column(db.DateTime, nullable=True, comment='Date and time of last login')
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
