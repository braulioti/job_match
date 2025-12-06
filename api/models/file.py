"""
File Model
Model for storing file metadata
"""

from api.models.base_model import BaseModel
from api.database.database import db


class File(BaseModel):
    """File model for storing file metadata"""
    __tablename__ = 'file'
    
    original_file_name = db.Column(db.String(200), nullable=False, comment='Original name of the uploaded file')
    hash = db.Column(db.String(40), nullable=False, unique=True, comment='SHA-1 hash of the file content')
    extension = db.Column(db.String(15), nullable=True, comment='File extension (e.g., .pdf, .docx)')
    content = db.Column(db.Text, nullable=True, comment='Full text content converted to TXT')
    
    def __repr__(self):
        return f"<File(id={self.id}, original_file_name={self.original_file_name}, hash={self.hash[:8]}...)>"

