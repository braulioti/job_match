"""
Ollama Provider
Provider for Ollama LLM integration
"""

import os
import requests
from typing import Optional, Dict, Any
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
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
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
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")
    
    def chat(self, messages: list, **kwargs) -> Dict[str, Any]:
        """
        Chat with Ollama using messages
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters (stream, temperature, etc.)
        
        Returns:
            Dict containing the response from Ollama
        """
        if not self.is_initialized():
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        url = f"{self._base_url}/api/chat"
        payload = {
            "model": self._model,
            "messages": messages,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")
    
    def _dividir_em_chunks(self, texto: str, tamanho: int = 6000) -> list:
        """
        Divide texto em chunks de tamanho especificado
        
        Args:
            texto: Texto a ser dividido
            tamanho: Tamanho de cada chunk em caracteres
        
        Returns:
            Lista de chunks
        """
        return [texto[i:i+tamanho] for i in range(0, len(texto), tamanho)]
    
    def _gerar_resumo_chunk(self, chunk: str, prompt_base: str) -> str:
        """
        Gera resumo de um chunk usando Ollama
        
        Args:
            chunk: Texto do chunk a ser resumido
            prompt_base: Prompt base para o resumo
        
        Returns:
            Resumo do chunk
        """
        url = f"{self._base_url}/api/generate"
        payload = {
            "model": self._model,
            "prompt": f"{prompt_base}\n\n{chunk}",
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")
    
    def generate_with_file(self, prompt: str, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Generate text using Ollama with a file attachment via multipart/form-data
        Processes large files by dividing them into chunks and generating a final summary
        
        Args:
            prompt: The prompt to send to the model
            file_path: Path to the file to attach
            **kwargs: Additional parameters (stream, temperature, etc.)
        
        Returns:
            Dict containing the response from Ollama
        """
        if not self.is_initialized():
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                texto = f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}")
        
        # Divide file into chunks (6000 characters per chunk)
        chunks = self._dividir_em_chunks(texto, tamanho=6000)
        
        if len(chunks) == 0:
            raise RuntimeError("File is empty")
        
        # Process each chunk
        analises = []
        prompt_analise = "Me mostre os dados pessoais do candidado e qual o percentual de aderencia a vaga. Detalhe os requisitos que ele não cumpriu. Analise o seguinte trecho:"
        
        for i, chunk in enumerate(chunks, start=1):
            print(f"Processando parte {i}/{len(chunks)}...")
            analise = self._gerar_resumo_chunk(chunk, prompt_analise)
            analises.append(analise)
        
        # Generate final analysis based on chunk analyses
        print("\nGerando análise final...")
        texto_analises = "\n\n------\n\n".join(analises)
        prompt_final = (
            "Com base nas análises abaixo, me mostre os dados pessoais do candidado e qual o percentual de aderencia a vaga. Detalhe os requisitos que ele não cumpriu. Produza uma análise final coerente e bem estruturada:\n\n" +
            texto_analises
        )
        
        url = f"{self._base_url}/api/generate"
        payload = {
            "model": self._model,
            "prompt": prompt_final,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            resultado = response.json()
            
            # Return response with additional metadata
            return {
                "response": resultado.get("response", ""),
                "model": resultado.get("model", self._model),
                "created_at": resultado.get("created_at", ""),
                "done": resultado.get("done", True),
                "chunks_processed": len(chunks),
                "full_response": resultado
            }
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available models in Ollama
        
        Returns:
            Dict containing the list of available models
        """
        if not self.is_initialized():
            raise RuntimeError("Provider not initialized. Call initialize() first.")
        
        url = f"{self._base_url}/api/tags"
        
        try:
            response = requests.get(url, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling Ollama API: {e}")

