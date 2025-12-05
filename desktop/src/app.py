"""
Main Application Class
Handles application initialization and main window
"""

import tkinter as tk
from tkinter import ttk
from src.ui.main_window import MainWindow
from src.utils.helpers import center_window
from src.config.settings import Settings
from src.database.db import initialize_database


class JobMatchApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        # Initialize database
        self._initialize_database()
        
        self.root = tk.Tk()
        self.root.title("Job Match")
        self.root.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}")
        
        # Set window icon
        self._set_window_icon()
        
        # Configure style
        self._configure_style()
        
        # Create main window
        self.main_window = MainWindow(self.root)
        
        # Center the window after widgets are created
        self.root.update_idletasks()
        center_window(self.root, Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    
    def _initialize_database(self):
        """Initialize the SQLite database"""
        Settings.initialize_directories()
        if initialize_database():
            print(f"Banco de dados inicializado: {Settings.get_db_path()}")
        else:
            print(f"Erro ao inicializar banco de dados: {Settings.get_db_path()}")
    
    def _set_window_icon(self):
        """Set the window icon"""
        try:
            favicon_path = Settings.get_favicon_path()
            if favicon_path.exists():
                self.root.iconbitmap(str(favicon_path))
        except Exception as e:
            print(f"Erro ao definir ícone da janela: {e}")
    
    def _configure_style(self):
        """Configure application style"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

