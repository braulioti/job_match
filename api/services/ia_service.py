"""
IA Service
Business logic for AI/ML processing operations
"""

import os
from pathlib import Path
from typing import Dict, Any
from integration.provider.ollama_provider import OllamaProvider


class IAService:
    """Service for IA operations"""
    
    def __init__(self):
        """
        Initialize the IA service
        Initializes the Ollama provider
        """
        self._ollama_provider = OllamaProvider()
        
        # Initialize the provider
        if not self._ollama_provider.initialize():
            raise RuntimeError(
                "Failed to initialize Ollama provider. Make sure Ollama is running."
            )
    
    def process(self, ia_model: str) -> Dict[str, Any]:
        """
        Process data using the specified IA model
        
        Args:
            ia_model: Model name to use (e.g., "ollama")
        
        Returns:
            Dictionary containing processing results
        
        Raises:
            ValueError: If ia_model is not supported
            RuntimeError: If provider is not initialized
        """
        # Normalize to lowercase for comparison
        ia_model_lower = ia_model.lower()
        
        # Route to appropriate processor based on model
        if ia_model_lower == 'ollama':
            return self.process_with_ollama()
        else:
            raise ValueError(f'Unsupported iaModel: {ia_model}. Supported models: ollama')
    
    def process_with_ollama(self) -> Dict[str, Any]:
        """
        Process data using Ollama provider
        
        Returns:
            Dictionary containing processing results
        
        Raises:
            RuntimeError: If Ollama provider is not initialized
        """
        # Verify that provider is initialized
        if not self._ollama_provider.is_initialized():
            raise RuntimeError(
                "Ollama provider is not initialized. Make sure Ollama is running."
            )
        
        # Implement chat with Ollama using file upload via multipart/form-data
        # System message defining the AI's role
        prompt = "Você é um especialista em RH capaz de analisar currículos e vagas. Avalie o arquivo anexo que contem os detalhes da vaga e os detalhes do currículo"
        
        # Get the path to arquivo_modelo.txt
        # Assuming the file is in the api root directory
        api_root = Path(__file__).parent.parent
        file_path = api_root / 'arquivo_modelo.txt'
        
        if not file_path.exists():
            raise RuntimeError(f"File not found: {file_path}")
        
        # Call Ollama generate API with file via multipart/form-data
        try:
            generate_response = self._ollama_provider.generate_with_file(
                prompt=prompt,
                file_path=str(file_path)
            )
            
            # Extract response content (already in the response dict)
            response_content = generate_response.get('response', '')
            chunks_processed = generate_response.get('chunks_processed', 0)
            
            result = {
                'provider': 'ollama',
                'model': self._ollama_provider.model,
                'base_url': self._ollama_provider.base_url,
                'response': response_content,
                'chunks_processed': chunks_processed,
                'full_response': generate_response.get('full_response', generate_response)
            }
        except Exception as e:
            raise RuntimeError(f"Error processing with Ollama: {str(e)}")
        
        return result
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the request data attributes
        
        Args:
            data: Dictionary containing the request data to validate
                Must contain only:
                - iaModel: Model name (must be "ollama")
        
        Returns:
            Dictionary containing validation results with:
                - valid: Boolean indicating if data is valid
                - errors: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Validate that data is provided
        if not data:
            errors.append('Request body is required')
            return {
                'valid': False,
                'errors': errors
            }
        
        # Validate that only iaModel is present
        allowed_keys = {'iaModel'}
        received_keys = set(data.keys())
        
        if received_keys != allowed_keys:
            extra_keys = received_keys - allowed_keys
            missing_keys = allowed_keys - received_keys
            if extra_keys:
                errors.append(f'Unexpected keys: {", ".join(sorted(extra_keys))}')
            if missing_keys:
                errors.append(f'Missing required keys: {", ".join(sorted(missing_keys))}')
        
        # Validate iaModel value
        ia_model = data.get('iaModel')
        if not ia_model:
            errors.append('iaModel is required')
        else:
            # Normalize to lowercase for comparison
            ia_model_lower = ia_model.lower()
            if ia_model_lower != 'ollama':
                errors.append(f'Invalid iaModel value: {ia_model}. Must be "ollama"')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def get_ollama_provider(self) -> OllamaProvider:
        """
        Get the current Ollama provider instance
        
        Returns:
            OllamaProvider instance
        """
        return self._ollama_provider
    
    def reset_provider(self):
        """
        Reset and reinitialize the provider instance
        (useful for testing or reinitialization)
        """
        self._ollama_provider = OllamaProvider()
        if not self._ollama_provider.initialize():
            raise RuntimeError(
                "Failed to reinitialize Ollama provider. Make sure Ollama is running."
            )

