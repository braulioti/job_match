"""
Main Application Class
Handles application initialization and main window
"""

import tkinter as tk
from tkinter import ttk
from src.ui.main_window import MainWindow
from src.ui.splash_screen import SplashScreen
from src.utils.helpers import center_window
from src.config.settings import Settings
from src.database.db import initialize_database
from src.manager.config_manager import ConfigManager
from src.manager.server_manager import ServerManager


class JobMatchApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window initially
        
        # Create and show splash screen
        self.splash = SplashScreen(self.root)
        self.splash.update_progress(10, "Inicializando aplicação...")
        self.root.update()
        
        # Initialize config file
        self.splash.update_progress(20, "Carregando configurações...")
        self._initialize_config()
        
        # Initialize servers
        self.splash.update_progress(40, "Carregando servidores...")
        self._initialize_servers()
        
        # Initialize database
        self.splash.update_progress(60, "Inicializando banco de dados...")
        self._initialize_database()
        
        # Configure main window
        self.splash.update_progress(80, "Configurando interface...")
        self.root.title("Job Match")
        self.root.geometry(f"{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}")
        
        # Set window icon
        self._set_window_icon()
        
        # Configure style
        self._configure_style()
        
        # Create main window
        self.splash.update_progress(90, "Carregando componentes...")
        self.main_window = MainWindow(
            self.root,
            server_manager=self.server_manager,
            config_manager=self.config_manager,
            selected_server=self.selected_server,
            on_server_changed=self._on_server_changed
        )
        
        # Finalize
        self.splash.update_progress(100, "Concluído!")
        self.root.update()
        
        # Close splash and show main window
        self.root.after(500, self._show_main_window)
    
    def _initialize_config(self):
        """Initialize config.ini file"""
        self.config_manager = ConfigManager()
    
    def _initialize_servers(self):
        """Initialize servers from servers file"""
        self.server_manager = ServerManager()
        
        server_url = self.config_manager.get('Server', 'url', fallback='')
        
        selected_server = None
        if server_url:
            selected_server = self.server_manager.get_server_by_url(server_url)
        
        if not selected_server:
            selected_server = self.server_manager.get_default_server()
            # Save the default server URL to config.ini if server was found
            if selected_server:
                self.config_manager.set('Server', 'url', selected_server['url'])
                self.config_manager.save()
        
        self.selected_server = selected_server
    
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
    
    def _on_server_changed(self, new_server):
        """
        Handle server change from configuration dialog
        
        Args:
            new_server: New ServerInterface selected
        """
        self.selected_server = new_server
        # Update main window's selected_server reference
        if self.main_window:
            self.main_window.selected_server = new_server
    
    def _show_main_window(self):
        """Close splash screen and show main window"""
        if self.splash:
            self.splash.close()
        
        # Show and maximize main window
        self.root.deiconify()
        self.root.update_idletasks()
        # Maximize window (works on Windows and Linux)
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

