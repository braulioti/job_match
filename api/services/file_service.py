"""
File Service
Business logic for file operations
"""

import os
import uuid
import tempfile
import warnings
from pathlib import Path
from typing import Dict, Any, Optional

# Configure Hugging Face Hub environment variables before importing docling
# This suppresses warnings about symlinks (Windows) and Xet Storage
if 'HF_HUB_DISABLE_SYMLINKS_WARNING' not in os.environ:
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Suppress Xet Storage warnings (optional package for better performance)
warnings.filterwarnings('ignore', message='.*Xet Storage.*', category=UserWarning)
warnings.filterwarnings('ignore', message='.*hf_xet.*', category=UserWarning)
warnings.filterwarnings('ignore', message='.*symlink.*', category=UserWarning)

from werkzeug.utils import secure_filename
from docling.document_converter import DocumentConverter

from api.database.database import db
from api.dto.file_data_dto import FileDataDTO
from api.models.file import File


class FileService:
    """Service for file operations"""

    def __init__(self):
        """Initialize FileService with DocumentConverter"""
        # Initialize document converter
        # docling automatically handles PDF and DOCX formats
        # Warnings are suppressed at module level
        self.converter = None
        self._init_converter()

    def _init_converter(self):
        """Initialize DocumentConverter with error handling for Windows symlink issues"""
        try:
            self.converter = DocumentConverter()
        except (OSError, PermissionError) as e:
            error_msg = str(e)
            if '1314' in error_msg or 'privilege' in error_msg.lower() or 'symlink' in error_msg.lower():
                # Try to clear problematic cache
                try:
                    import shutil
                    cache_path = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub')
                    model_cache = os.path.join(cache_path, 'models--docling-project--docling-layout-heron')
                    if os.path.exists(model_cache):
                        shutil.rmtree(model_cache)
                        # Retry after clearing cache
                        self.converter = DocumentConverter()
                        return
                except:
                    pass
                raise Exception(
                    f'Symlink permission error on Windows. '
                    f'Please see api/TROUBLESHOOTING_DOCLING.md for solutions. '
                    f'Quick fix: Delete folder: %USERPROFILE%\\.cache\\huggingface\\hub\\models--docling-project--docling-layout-heron'
                )
            raise

    def _convert_file_to_text(self, file_content: bytes, file_extension: str) -> str:
        """
        Convert file content to plain text using docling
        
        Args:
            file_content: File content as bytes
            file_extension: File extension (e.g., '.pdf', '.docx')
            
        Returns:
            Extracted text from file
            
        Raises:
            Exception: If file conversion fails
        """
        file_extension = file_extension.lower()
        
        # Supported formats
        if file_extension not in ['.pdf', '.docx']:
            raise Exception(f'Unsupported file format: {file_extension}. Supported formats: .pdf, .docx')
        
        try:
            # Create a temporary file to save the content
            # docling works better with file paths than BytesIO
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Convert document using docling
                result = self.converter.convert(temp_file_path)
                
                # Extract text from the result in markdown format
                # docling provides markdown output which is clean and structured
                extracted_text = result.document.export_to_markdown()
                
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
                return extracted_text
                
            except (OSError, PermissionError) as e:
                # Handle Windows symlink permission errors
                error_msg = str(e)
                if '1314' in error_msg or 'privilege' in error_msg.lower() or 'symlink' in error_msg.lower():
                    # Clear problematic cache and retry once
                    try:
                        cache_path = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub')
                        if os.path.exists(cache_path):
                            # Try to remove only the problematic model cache
                            import shutil
                            model_cache = os.path.join(cache_path, 'models--docling-project--docling-layout-heron')
                            if os.path.exists(model_cache):
                                try:
                                    shutil.rmtree(model_cache)
                                    # Retry conversion after clearing cache
                                    result = self.converter.convert(temp_file_path)
                                    extracted_text = result.document.export_to_markdown()
                                    if os.path.exists(temp_file_path):
                                        os.unlink(temp_file_path)
                                    return extracted_text
                                except:
                                    pass
                    except:
                        pass
                    
                    raise Exception(
                        f'Symlink permission error on Windows. '
                        f'Please see api/TROUBLESHOOTING_DOCLING.md for solutions. '
                        f'Quick fix: Delete the cache folder: %USERPROFILE%\\.cache\\huggingface\\hub\\models--docling-project--docling-layout-heron '
                        f'Error details: {error_msg}'
                    )
                
                # Clean up temporary file in case of error
                if os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                raise Exception(f'Failed to extract text using docling: {str(e)}')
                
            except Exception as e:
                # Clean up temporary file in case of error
                if os.path.exists(temp_file_path):
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                raise Exception(f'Failed to extract text using docling: {str(e)}')
                
        except Exception as e:
            raise Exception(f'Failed to convert {file_extension} to text: {str(e)}')

    def _save_file(self, file, hash: str, extension: str) -> str:
        """
        Save uploaded file to disk in the files directory

        Args:
            file: File object from Flask request.files (FileStorage) or bytes
            hash: File hash (UUID) to use as filename
            extension: File extension (e.g., '.pdf', '.docx')

        Returns:
            Full path to the saved file

        Raises:
            Exception: If file saving fails
        """
        try:
            # Get project root directory (1 level up from api/services/)
            project_root = Path(__file__).parent.parent

            # Define files directory path
            files_dir = project_root / 'files'

            # Create files directory if it doesn't exist
            files_dir.mkdir(parents=True, exist_ok=True)

            # Build file path: hash + extension
            file_name = f"{hash}{extension}" if extension else hash
            file_path = files_dir / file_name

            # Reset file pointer to beginning
            if hasattr(file, 'seek'):
                file.seek(0)

            # Read file content if it's a FileStorage object
            if hasattr(file, 'read'):
                file_content = file.read()
            elif isinstance(file, bytes):
                file_content = file
            else:
                raise ValueError(f'Unsupported file type: {type(file)}')

            # Write file to disk
            with open(file_path, 'wb') as f:
                f.write(file_content)

            # Reset file pointer again for potential future use
            if hasattr(file, 'seek'):
                file.seek(0)

            return str(file_path.resolve())

        except Exception as e:
            raise Exception(f'Failed to save file to disk: {str(e)}')
    
    def validate_file(self, file) -> FileDataDTO:
        """
        Validate file object before processing
        
        Args:
            file: File object from Flask request.files (FileStorage)
            
        Returns:
            Validated data and TXT file content
                
        Raises:
            ValueError: If validation fails
        """

        # Validate file object exists
        if not file:
            raise ValueError('File is required')
        
        # Validate filename
        if not file.filename or file.filename == '':
            raise ValueError('File name is required')

        original_file_name = secure_filename(file.filename)
        file_extension = os.path.splitext(original_file_name)[1].lower() if '.' in original_file_name else ''
        
        file.seek(0)
        file_content = file.read()
        file.seek(0)
        
        # Convert DOCX or PDF to plain text using docling
        if file_extension in ['.pdf', '.docx']:
            try:
                content = self._convert_file_to_text(file_content, file_extension)
            except Exception as e:
                raise ValueError(f'Failed to convert file to text: {str(e)}')
        else:
            raise ValueError(f'Invalid file extension. Supported formats: .pdf, .docx')

        return FileDataDTO(
            original_file_name = original_file_name,
            extension = file_extension,
            hash = str(uuid.uuid4()),
            content = content,
            file = file  # Store the file object
        )

    def create_file(self, file_data: FileDataDTO) -> Dict[str, Any]:
        """
        Create a new file record and save file to disk

        Args:
            file_data: Validated data and content extracted from the file

        Returns:
            Dictionary with file data
        """
        
        # Save file to disk first
        if file_data.file is not None:
            try:
                self._save_file(
                    file=file_data.file,
                    hash=file_data.hash,
                    extension=file_data.extension
                )
            except Exception as e:
                raise Exception(f'Failed to save file to disk: {str(e)}')

        new_file = File(
            original_file_name=file_data.original_file_name,
            hash=file_data.hash,
            extension=file_data.extension,
            content=file_data.content
        )

        try:
            db.session.add(new_file)
            db.session.commit()

            return {
                'original_file_name': new_file.original_file_name,
                'hash': new_file.hash,
                'created_at': new_file.created_at.isoformat() if new_file.created_at else None,
                'updated_at': new_file.updated_at.isoformat() if new_file.updated_at else None
            }

        except Exception as e:
            db.session.rollback()
            raise Exception(f'Failed to save file to database: {str(e)}')


