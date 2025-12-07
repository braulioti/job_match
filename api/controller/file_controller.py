"""
File Controller
Handles file upload operations
"""

from typing import Dict, Any, Tuple

from api.services.file_service import FileService


class FileController:
    """Controller for file operations"""
    
    @staticmethod
    def upload_file(file) -> Tuple[Dict[str, Any], int]:
        """
        Handle file upload
        
        Args:
            file: File object from Flask request.files
            
        Returns:
            Tuple containing:
                - response_dict: Response dictionary
                - status_code: HTTP status code
        """
        try:
            file_service = FileService()
            file_data = file_service.validate_file(file=file)
            return file_service.create_file(file_data), 201
            
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

