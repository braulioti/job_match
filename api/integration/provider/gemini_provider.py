"""
Gemini Provider
Provider for Google Gemini LLM integration
"""

import os
from typing import Optional

import google.generativeai as genai

from .base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """Provider for Google Gemini LLM integration"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Gemini provider
        
        Args:
            api_key: Google API key for Gemini (defaults to environment variable)
            model: Model name to use (defaults to environment variable or 'gemini-pro')
        """
        super().__init__()
        self._api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self._model_name = model or os.environ.get('GEMINI_MODEL', 'gemini-pro')
        self._timeout = int(os.environ.get('GEMINI_TIMEOUT', '30'))
        
        if not self._api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure the API key
        genai.configure(api_key=self._api_key)
        self._model = None
    
    @property
    def api_key(self) -> str:
        """Get the API key"""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str):
        """Set the API key"""
        self._api_key = value
        genai.configure(api_key=value)
    
    @property
    def model(self) -> str:
        """Get the model name"""
        return self._model_name
    
    @model.setter
    def model(self, value: str):
        """Set the model name"""
        self._model_name = value
        if self._initialized:
            self._model = genai.GenerativeModel(value)
    
    def initialize(self):
        """
        Initialize the Gemini provider
        Checks if API key is valid and model is accessible
        """
        try:
            if not self._api_key:
                self._initialized = False
                return False
            
            # Configure the API key
            genai.configure(api_key=self._api_key)
            
            # Try to load the model
            self._model = genai.GenerativeModel(self._model_name)
            
            # Test with a simple prompt to verify API access
            try:
                self._model.generate_content(
                    "Test",
                    request_options={"timeout": 5}
                )
                self._initialized = True
                return True
            except Exception as e:
                print(f"Error testing Gemini API: {e}")
                self._initialized = False
                return False
        except Exception as e:
            print(f"Error initializing Gemini provider: {e}")
            self._initialized = False
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Gemini
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters (temperature, max_output_tokens, etc.)
        
        Returns:
            Dict containing the response from Gemini
        """
        if not self.is_initialized():
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        if self._model is None:
            self._model = genai.GenerativeModel(self._model_name)
        
        try:
            generation_config = {}
            if 'temperature' in kwargs:
                generation_config['temperature'] = kwargs.pop('temperature')
            if 'max_output_tokens' in kwargs:
                generation_config['max_output_tokens'] = kwargs.pop('max_output_tokens')
            if 'top_p' in kwargs:
                generation_config['top_p'] = kwargs.pop('top_p')
            if 'top_k' in kwargs:
                generation_config['top_k'] = kwargs.pop('top_k')

            if generation_config:
                config = genai.types.GenerationConfig(**generation_config)
                kwargs['generation_config'] = config

            request_options = kwargs.pop('request_options', {})
            request_options['timeout'] = request_options.get('timeout', self._timeout)
            kwargs['request_options'] = request_options

            response = self._model.generate_content(prompt, **kwargs)
            
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {e}")
