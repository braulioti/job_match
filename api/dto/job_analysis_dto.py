"""
Job Analysis DTO
Data Transfer Object for job analysis requests
"""

from dataclasses import dataclass
from enum import Enum


class IAModelEnum(str, Enum):
    """Enum for IA model types"""
    OLLAMA = "ollama"
    GEMINI = "gemini"


@dataclass
class JobAnalysisDTO:
    """Data Transfer Object for job analysis requests"""
    
    ia_model: IAModelEnum
    job_vacancy: str
    resume: str
    
    def __post_init__(self):
        """Validate the DTO after initialization"""
        if not isinstance(self.ia_model, IAModelEnum):
            if isinstance(self.ia_model, str):
                # Try to convert string to enum
                try:
                    self.ia_model = IAModelEnum(self.ia_model.lower())
                except ValueError:
                    raise ValueError(
                        f"ia_model must be one of {[e.value for e in IAModelEnum]}. "
                        f"Got: {self.ia_model}"
                    )
            else:
                raise TypeError(
                    f"ia_model must be a string or IAModelEnum enum. "
                    f"Got: {type(self.ia_model)}"
                )
        
        if not isinstance(self.job_vacancy, str):
            raise TypeError(f"job_vacancy must be a string. Got: {type(self.job_vacancy)}")
        
        if not isinstance(self.resume, str):
            raise TypeError(f"resume must be a string. Got: {type(self.resume)}")
        
        if not self.job_vacancy.strip():
            raise ValueError("job_vacancy cannot be empty")
        
        if not self.resume.strip():
            raise ValueError("resume cannot be empty")
