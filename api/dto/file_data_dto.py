"""
File Data DTO
Data Transfer Object for file data
"""

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class FileDataDTO:
    """File structure"""
    original_file_name: str
    extension: str
    hash: str
    content: str
    file: Optional[Any] = None  # File object or file content in bytes
