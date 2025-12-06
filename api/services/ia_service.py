"""
IA Service
Business logic for AI/ML processing operations
"""

from typing import Dict, Any

from api.config.settings import Config
from api.dto import JobAnalysisDTO, IAModelEnum
from api.integration.provider import GeminiProvider, BaseProvider
from api.integration.provider.ollama_provider import OllamaProvider


class IAService:
    """Service for IA operations"""
    
    def __init__(self):
        """
        Initialize the IA service
        Providers are initialized lazily when needed
        """
        self._ollama_provider = None
        self._gemini_provider = None
    
    def process(self, job_analysis_dto: JobAnalysisDTO) -> Dict[str, Any]:
        """
        Process data using the specified IA model
        
        Args:
            job_analysis_dto: JobAnalysisDTO containing the analysis request data
        
        Returns:
            Dictionary containing processing results
        
        Raises:
            ValueError: If ia_model is not supported
            RuntimeError: If provider is not initialized
        """
        if job_analysis_dto.ia_model == IAModelEnum.OLLAMA:
            if self._ollama_provider is None:
                self._ollama_provider = OllamaProvider()
            if not self._ollama_provider.is_initialized():
                if not self._ollama_provider.initialize():
                    raise RuntimeError(
                        "Failed to initialize Ollama provider. Make sure Ollama is running and accessible."
                    )
            return self._process_with_provider(job_analysis_dto, self._ollama_provider)
        elif job_analysis_dto.ia_model == IAModelEnum.GEMINI:
            if self._gemini_provider is None:
                self._gemini_provider = GeminiProvider()
            if not self._gemini_provider.is_initialized():
                if not self._gemini_provider.initialize():
                    raise RuntimeError(
                        "Failed to initialize Gemini provider. Make sure GEMINI_API_KEY is set correctly."
                    )
            return self._process_with_provider(job_analysis_dto, self._gemini_provider)
        else:
            raise ValueError(f'Unsupported iaModel: {job_analysis_dto.ia_model.value}.')
    
    def _process_with_provider(self, job_analysis_dto: JobAnalysisDTO, provider: BaseProvider) -> Dict[str, Any]:
        """
        Process data using Ollama provider
        
        Args:
            job_analysis_dto: JobAnalysisDTO containing the analysis request data
            provider: Provider that will be used to process
        
        Returns:
            Dictionary containing processing results
        
        Raises:
            RuntimeError: If Ollama provider is not initialized
        """
        if not provider.is_initialized():
            raise RuntimeError("Provider is not initialized. Make sure provider is running.")

        try:
            prompt_file_path = Config.PROMPT_JOB_ANALYS

            # Build prompt with replacements
            prompt = provider.build_prompt(
                prompt_file_path,
                {
                    "job_vacancy": job_analysis_dto.job_vacancy,
                    "resume": job_analysis_dto.resume
                }
            )

            generate_response = provider.generate(prompt=prompt)
            result = provider.get_json(text=generate_response)
        except Exception as e:
            raise RuntimeError(f"Error processing with Provider: {str(e)}")
        
        return result
