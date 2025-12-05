"""
Database Management
Handles SQLite database initialization and operations
"""

import sqlite3
import sys
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
    
    def _get_scripts_path(self):
        """Get the path to the scripts directory"""
        # Quando executado como PyInstaller bundle, usar sys._MEIPASS
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Executando como executável PyInstaller
            base_path = Path(sys._MEIPASS)
        else:
            # Executando em desenvolvimento
            # desktop/src/database/db.py -> desktop/scripts
            # Subir 3 níveis: database -> src -> desktop
            base_path = Path(__file__).parent.parent.parent
        
        return base_path / "scripts"
    
    def _execute_sql_script(self, cursor, script_path):
        """
        Execute a SQL script file
        
        Args:
            cursor: Database cursor
            script_path: Path to the SQL script file
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Remove linhas vazias e comentários de linha única
            lines = []
            for line in script_content.split('\n'):
                stripped = line.strip()
                # Ignora linhas vazias e comentários que começam com --
                if stripped and not stripped.startswith('--'):
                    # Remove comentários inline (-- comentário no final da linha)
                    if '--' in stripped:
                        # Verifica se não está dentro de uma string
                        comment_pos = stripped.find('--')
                        # Se houver aspas antes do comentário, pode ser uma string
                        # Por simplicidade, assumimos que -- no final da linha é comentário
                        if comment_pos > 0:
                            stripped = stripped[:comment_pos].strip()
                    if stripped:
                        lines.append(stripped)
            
            # Junta as linhas e executa o script
            clean_script = '\n'.join(lines)
            if clean_script.strip():
                # Executa cada statement separado por ponto e vírgula
                statements = [stmt.strip() for stmt in clean_script.split(';') if stmt.strip()]
                for statement in statements:
                    cursor.execute(statement)
        except Exception as e:
            print(f"Erro ao executar script {script_path.name}: {e}")
            raise
    
    def initialize(self):
        """Initialize database schema by executing SQL scripts from scripts folder"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            scripts_path = self._get_scripts_path()
            
            if not scripts_path.exists():
                print(f"Pasta de scripts não encontrada: {scripts_path}")
                conn.commit()
                return False
            
            sql_files = sorted(scripts_path.glob("*.sql"))
            
            if not sql_files:
                print(f"Nenhum arquivo SQL encontrado em: {scripts_path}")
                conn.commit()
                return False
            
            for sql_file in sql_files:
                print(f"Executando script: {sql_file.name}")
                self._execute_sql_script(cursor, sql_file)
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            conn.rollback()
            return False
        except Exception as e:
            print(f"Erro ao executar scripts SQL: {e}")
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

