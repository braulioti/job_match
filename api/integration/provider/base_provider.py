"""
Base Provider
Base class for all provider classes
"""

import json
import os
import re
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProvider(ABC):
    """Base class for all provider classes"""
    
    def __init__(self):
        """Initialize the base provider"""
        self._initialized = False
    
    @property
    def initialized(self):
        """Get the initialization status"""
        return self._initialized
    
    @initialized.setter
    def initialized(self, value):
        """Set the initialization status"""
        self._initialized = value
    
    @abstractmethod
    def initialize(self):
        """
        Initialize the provider
        Must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the provider
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters (stream, temperature, etc.)
        
        Returns:
            Response string containing the response from the provider
        
        Must be implemented by subclasses
        """
        pass
    
    def is_initialized(self):
        """
        Check if the provider is initialized
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized
    
    def build_prompt(self, prompt_file: str, replacements: Dict[str, str] = None) -> str:
        """
        Build a prompt by reading a file and replacing placeholders
        
        Args:
            prompt_file (str): Path to the prompt file
            replacements (Dict[str, str]): Dictionary with key-value pairs to replace
                                          Keys should match placeholders in format {{key}}
                                          Example: {"dados_vaga": "texto da vaga"}
        
        Returns:
            str: The processed prompt with replacements applied
        
        Raises:
            FileNotFoundError: If the prompt file doesn't exist
            IOError: If there's an error reading the file
        """
        prompt_text = ""
        if replacements is None:
            replacements = {}
        
        # Read the prompt file
        if not os.path.exists(prompt_file):
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        
        # Replace placeholders in format {{key}} with values from replacements
        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            prompt_text = prompt_text.replace(placeholder, value)
        
        return prompt_text

    def get_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from Gemini response text and return as dictionary

        Args:
            text: Response text that may contain JSON in markdown code blocks or as plain JSON

        Returns:
            Dictionary containing the parsed JSON data

        Raises:
            ValueError: If no valid JSON can be extracted from the text
            json.JSONDecodeError: If the extracted JSON is invalid
        """
        if not text:
            raise ValueError("Text is empty")

        # Try to extract JSON from markdown code blocks (```json\n...\n``` or ```json...```)
        # Handles both ```json\n...\n``` and ```\n...\n``` formats
        json_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        matches = re.findall(json_pattern, text, re.DOTALL)

        if matches:
            # Use the first match
            json_str = matches[0].strip()
        else:
            # Try to find JSON object directly in the text
            # Look for content between { and }
            brace_start = text.find('{')
            brace_end = text.rfind('}')

            if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
                json_str = text[brace_start:brace_end + 1]
            else:
                # If no JSON structure found, try parsing the whole text
                json_str = text.strip()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from text: {e}. Text: {json_str[:200]}")

