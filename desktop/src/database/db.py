"""
Database Management
Handles SQLite database initialization and operations
"""

import sqlite3
from pathlib import Path
from src.config.settings import Settings


class Database:
    """Database management class"""
    
    def __init__(self, db_path=None):
        """
        Initialize database connection
        
        Args:
            db_path: Path to database file (if None, uses Settings.get_db_path())
        """
        self.db_path = db_path or Settings.get_db_path()
        self.connection = None
    
    def connect(self):
        """Create database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize(self):
        """Initialize database schema"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Criar tabelas básicas
            # Você pode adicionar mais tabelas conforme necessário
            
            # Exemplo de tabela (pode ser expandida conforme necessário)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Adicione mais tabelas aqui conforme necessário
            # Por exemplo:
            # cursor.execute("""
            #     CREATE TABLE IF NOT EXISTS jobs (
            #         id INTEGER PRIMARY KEY AUTOINCREMENT,
            #         project_id INTEGER,
            #         title TEXT NOT NULL,
            #         description TEXT,
            #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            #         FOREIGN KEY (project_id) REFERENCES projects(id)
            #     )
            # """)
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            conn.rollback()
            return False
    
    def execute(self, query, params=None):
        """Execute a query"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            conn.rollback()
            raise
    
    def fetch_all(self, query, params=None):
        """Fetch all results from a query"""
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """Fetch one result from a query"""
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def __enter__(self):
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def initialize_database():
    """
    Initialize the database on application startup
    Returns True if successful, False otherwise
    """
    db = Database()
    try:
        # Garantir que o diretório existe
        db_path = Path(db.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Inicializar banco de dados
        success = db.initialize()
        db.close()
        return success
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        return False

