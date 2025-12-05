"""
Project Entity
Represents a project in the system
"""

from typing import Optional, List
from dataclasses import dataclass
from src.database.db import Database


@dataclass
class Project:
    """Project entity"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @classmethod
    def create(cls, name: str, description: Optional[str] = None) -> 'Project':
        """
        Create a new project in the database
        
        Args:
            name: Project name
            description: Project description (optional)
            
        Returns:
            Project: Created project with ID
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO project (name, description) VALUES (?, ?)",
                (name, description if description else None)
            )
            project_id = cursor.lastrowid
            conn.commit()
            
            # Fetch the created project
            cursor.execute(
                "SELECT id, name, description, created_at, updated_at FROM project WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            else:
                # Fallback if fetch fails
                return cls(id=project_id, name=name, description=description)
        finally:
            db.close()
    
    @classmethod
    def get_all(cls, order_by: str = "name ASC") -> List['Project']:
        """
        Get all projects from database
        
        Args:
            order_by: SQL ORDER BY clause (default: "name ASC")
            
        Returns:
            List[Project]: List of all projects
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, name, description, created_at, updated_at FROM project ORDER BY {order_by}")
            rows = cursor.fetchall()
            
            projects = []
            for row in rows:
                projects.append(cls(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            
            return projects
        finally:
            db.close()
    
    @classmethod
    def get_by_id(cls, project_id: int) -> Optional['Project']:
        """
        Get a project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Optional[Project]: Project if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description, created_at, updated_at FROM project WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        finally:
            db.close()

