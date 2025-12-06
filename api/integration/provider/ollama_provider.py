"""
Ollama Provider
Provider for Ollama LLM integration
"""

import os
from typing import Optional

import requests

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """Provider for Ollama LLM integration"""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Ollama provider
        
        Args:
            base_url: Base URL for Ollama API (defaults to environment variable or http://localhost:11434)
            model: Model name to use (defaults to environment variable or 'llama2')
        """
        super().__init__()
        self._base_url = base_url or os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self._model = model or os.environ.get('OLLAMA_MODEL', 'llama2')
        self._timeout = int(os.environ.get('OLLAMA_TIMEOUT', '30'))
    
    @property
    def base_url(self) -> str:
        """Get the base URL"""
        return self._base_url
    
    @base_url.setter
    def base_url(self, value: str):
        """Set the base URL"""
        self._base_url = value
    
    @property
    def model(self) -> str:
        """Get the model name"""
        return self._model
    
    @model.setter
    def model(self, value: str):
        """Set the model name"""
        self._model = value
    
    def initialize(self):
        """
        Initialize the Ollama provider
        Checks if Ollama is available and accessible
        """
        try:
            # Check if Ollama is available
            response = requests.get(
                f"{self._base_url}/api/tags",
                timeout=self._timeout
            )
            if response.status_code == 200:
                self._initialized = True
                return True
            else:
                self._initialized = False
                return False
        except Exception as e:
            print(f"Error initializing Ollama provider: {e}")
            self._initialized = False
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters (stream, temperature, etc.)
        
        Returns:
            Dict containing the response from Ollama
        """
        if not self.is_initialized():
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        url = f"{self._base_url}/api/generate"
        payload = {
            "model": self._model,
            "prompt": prompt,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")

