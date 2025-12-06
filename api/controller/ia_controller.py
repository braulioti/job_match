"""
IA Controller
Handles AI/ML processing logic and exception handling
"""

from typing import Dict, Any, Tuple

from api.services.ia_service import IAService


class IAController:
    """Controller for IA operations"""
    
    @staticmethod
    def process(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Process data using AI/ML services
        
        Args:
            data: Dictionary containing the request data
                Must contain only:
                - iaModel: Model name (must be "ollama")
        
        Returns:
            Tuple containing:
                - response_dict: Response dictionary
                - status_code: HTTP status code
        """
        try:
            # Initialize service and validate request data
            ia_service = IAService()
            validation_result = ia_service.validate(data)
            
            if not validation_result['valid']:
                return {
                    'error': 'Validation failed',
                    'errors': validation_result['errors']
                }, 400
            
            # Get iaModel from request (camelCase)
            ia_model = data.get('iaModel')
            
            # Process using the specified model
            processed_data = ia_service.process(ia_model)
            
            return {
                'message': 'Processing completed',
                'status': 'success',
                'iaModel': ia_model,
                'data': processed_data
            }, 200
            
        except ValueError as e:
            # Handle validation errors
            return {
                'error': 'Validation error',
                'message': str(e)
            }, 400
            
        except Exception as e:
            # Handle unexpected errors
            return {
                'error': 'Internal server error',
                'message': str(e)
            }, 500
    

