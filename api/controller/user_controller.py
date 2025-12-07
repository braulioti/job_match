"""
User Controller
Handles user operations
"""

from typing import Dict, Any, Tuple

from api.services.user_service import UserService


class UserController:
    """Controller for user operations"""
    
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Handle user creation
        
        Args:
            data: Dictionary containing user data (email, password)
            
        Returns:
            Tuple containing:
                - response_dict: Response dictionary
                - status_code: HTTP status code
        """
        try:
            user_service = UserService()
            user_data = user_service.validate_user_data(data)
            return user_service.create_user(user_data), 201
            
        except ValueError as e:
            return {
                'error': 'Validation error',
                'message': str(e)
            }, 400
            
        except Exception as e:
            return {
                'error': 'Internal server error',
                'message': str(e)
            }, 500
