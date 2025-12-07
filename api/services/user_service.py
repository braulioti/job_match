"""
User Service
Business logic for user operations
"""

import uuid
from typing import Dict, Any

from werkzeug.security import generate_password_hash

from api.database.database import db
from api.dto.user_data_dto import UserDataDTO
from api.models.user import User


class UserService:
    """Service for user operations"""

    def __init__(self):
        """Initialize UserService"""
        pass

    def validate_user_data(self, data: Dict[str, Any]) -> UserDataDTO:
        """
        Validate user data before creating user
        
        Args:
            data: Dictionary containing user data (email, password)
            
        Returns:
            Validated and processed user data
            
        Raises:
            ValueError: If validation fails
        """
        if not data:
            raise ValueError('User data is required')
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate email
        if not email:
            raise ValueError('Email is required')
        
        if '@' not in email or '.' not in email.split('@')[1]:
            raise ValueError('Invalid email format')
        
        # Validate password
        if not password:
            raise ValueError('Password is required')
        
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        
        return UserDataDTO(email=email, password=password)

    def create_user(self, user_data: UserDataDTO) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            user_data: Validated user data (email, password)
            
        Returns:
            Dictionary with user data (excluding password)
            
        Raises:
            ValueError: If user already exists or validation fails
            Exception: If database operation fails
        """
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data.email).first()
        if existing_user:
            raise ValueError('User with this email already exists')

        hashed_password = generate_password_hash(user_data.password)
        auth_hash = str(uuid.uuid4())
        
        # Create new user
        new_user = User(
            email=user_data.email,
            password=hashed_password,
            hash=auth_hash
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            return {
                "email": new_user.email,
                "hash": new_user.hash
            }
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to create user: {str(e)}')

