"""
IA Controller
Handles AI/ML processing logic and exception handling
"""

import base64
from typing import Dict, Any, Tuple

from api.dto import JobAnalysisDTO
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
            ia_service = IAService()
            
            # Decode base64 strings to regular strings
            try:
                job_vacancy_b64 = data.get('jobVacancy', '')
                resume_b64 = data.get('resume', '')
                
                job_vacancy = base64.b64decode(job_vacancy_b64).decode('utf-8') if job_vacancy_b64 else ''
                resume = base64.b64decode(resume_b64).decode('utf-8') if resume_b64 else ''
            except Exception as e:
                return {
                    'error': 'Invalid base64 encoding',
                    'message': f'Failed to decode base64 data: {str(e)}'
                }, 400
            
            job_analysis_dto = JobAnalysisDTO(
                ia_model=data.get('iaModel'),
                job_vacancy=job_vacancy,
                resume=resume
            )
            
            processed_data = ia_service.process(job_analysis_dto)
            
            return processed_data, 200
            
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
    

