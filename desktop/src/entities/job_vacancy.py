"""
Job Vacancy Entity
Represents a job vacancy in the system
"""

from typing import Optional, List
from dataclasses import dataclass
from src.database.db import Database


@dataclass
class JobVacancy:
    """Job Vacancy entity"""
    id: Optional[int] = None
    project_id: int = 0
    title: str = ""
    description: Optional[str] = None
    resume_folder: Optional[str] = None
    
    @classmethod
    def create(cls, project_id: int, title: str, description: Optional[str] = None, resume_folder: Optional[str] = None) -> 'JobVacancy':
        """
        Create a new job vacancy in the database
        
        Args:
            project_id: Project ID (foreign key)
            title: Job vacancy title
            description: Job vacancy description (optional)
            resume_folder: Resume folder path (optional)
            
        Returns:
            JobVacancy: Created job vacancy with ID
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO job_vacancy (project_id, title, description, resume_folder) VALUES (?, ?, ?, ?)",
                (project_id, title, description if description else None, resume_folder if resume_folder else None)
            )
            job_vacancy_id = cursor.lastrowid
            conn.commit()
            
            # Fetch the created job vacancy
            cursor.execute(
                "SELECT id, project_id, title, description, resume_folder FROM job_vacancy WHERE id = ?",
                (job_vacancy_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row['id'],
                    project_id=row['project_id'],
                    title=row['title'],
                    description=row['description'],
                    resume_folder=row['resume_folder']
                )
            else:
                # Fallback if fetch fails
                return cls(id=job_vacancy_id, project_id=project_id, title=title, description=description, resume_folder=resume_folder)
        finally:
            db.close()
    
    @classmethod
    def get_all(cls, project_id: Optional[int] = None, order_by: str = "title ASC") -> List['JobVacancy']:
        """
        Get all job vacancies from database
        
        Args:
            project_id: Optional project ID to filter by
            order_by: SQL ORDER BY clause (default: "title ASC")
            
        Returns:
            List[JobVacancy]: List of all job vacancies
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            
            if project_id:
                cursor.execute(
                    f"SELECT id, project_id, title, description, resume_folder FROM job_vacancy WHERE project_id = ? ORDER BY {order_by}",
                    (project_id,)
                )
            else:
                cursor.execute(f"SELECT id, project_id, title, description, resume_folder FROM job_vacancy ORDER BY {order_by}")
            
            rows = cursor.fetchall()
            
            job_vacancies = []
            for row in rows:
                job_vacancies.append(cls(
                    id=row['id'],
                    project_id=row['project_id'],
                    title=row['title'],
                    description=row['description'],
                    resume_folder=row['resume_folder']
                ))
            
            return job_vacancies
        finally:
            db.close()
    
    @classmethod
    def get_by_id(cls, job_vacancy_id: int) -> Optional['JobVacancy']:
        """
        Get a job vacancy by ID
        
        Args:
            job_vacancy_id: Job vacancy ID
            
        Returns:
            Optional[JobVacancy]: Job vacancy if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        db = Database()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, project_id, title, description, resume_folder FROM job_vacancy WHERE id = ?",
                (job_vacancy_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return cls(
                    id=row['id'],
                    project_id=row['project_id'],
                    title=row['title'],
                    description=row['description'],
                    resume_folder=row['resume_folder']
                )
            return None
        finally:
            db.close()
    
    @classmethod
    def get_by_project_id(cls, project_id: int, order_by: str = "title ASC") -> List['JobVacancy']:
        """
        Get all job vacancies for a specific project
        
        Args:
            project_id: Project ID
            order_by: SQL ORDER BY clause (default: "title ASC")
            
        Returns:
            List[JobVacancy]: List of job vacancies for the project
            
        Raises:
            Exception: If database operation fails
        """
        return cls.get_all(project_id=project_id, order_by=order_by)

