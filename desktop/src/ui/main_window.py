"""
Main Window UI Component
"""

import tkinter as tk
from tkinter import ttk
from src.config.settings import Settings
from src.utils.helpers import center_window


class MainWindow:
    """Main window of the application"""
    
    def __init__(self, parent):
        """Initialize the main window"""
        self.parent = parent
        self._create_menu()
        self._create_widgets()
    
    def _create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        # Arquivo menu
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Projeto", menu=arquivo_menu)
        arquivo_menu.add_command(label="Sair", command=self._on_exit, accelerator="Ctrl+Q")
        
        # Ajuda menu
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self._show_about)
        
        # Bind keyboard shortcut
        self.parent.bind('<Control-q>', lambda e: self._on_exit())
    
    def _on_exit(self):
        """Handle exit menu item"""
        self.parent.quit()
    
    def _show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.parent)
        about_window.title("Sobre")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # Make window modal
        about_window.transient(self.parent)
        about_window.grab_set()
        about_window.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App name
        app_name_label = ttk.Label(
            main_frame,
            text=Settings.APP_NAME,
            font=('Segoe UI', 18, 'bold')
        )
        app_name_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(
            main_frame,
            text=f"Versão {Settings.APP_VERSION}",
            font=('Segoe UI', 10)
        )
        version_label.pack(pady=(0, 20))
        
        # Description
        description_text = (
            "Serviço de avaliação de currículos para avaliar o grau de "
            "aderência do currículo com a vaga."
        )
        description_label = ttk.Label(
            main_frame,
            text=description_text,
            font=('Segoe UI', 10),
            wraplength=350,
            justify=tk.CENTER
        )
        description_label.pack(pady=(0, 20))
        
        # Author
        author_label = ttk.Label(
            main_frame,
            text="Criado e mantido por Bráulio Figueiredo",
            font=('Segoe UI', 9)
        )
        author_label.pack(pady=(0, 10))
        
        # Website
        website_label = ttk.Label(
            main_frame,
            text="https://brau.io",
            font=('Segoe UI', 9),
            foreground='blue',
            cursor='hand2'
        )
        website_label.pack(pady=(0, 20))
        
        # Close button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        close_button = ttk.Button(
            button_frame,
            text="Fechar",
            command=about_window.destroy
        )
        close_button.pack()
        
        # Bind Enter key to close
        about_window.bind('<Return>', lambda e: about_window.destroy())
        about_window.bind('<Escape>', lambda e: about_window.destroy())
        
        # Center the window after widgets are created
        about_window.update_idletasks()
        center_window(about_window, 400, 300)
    
    def _create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_label = ttk.Label(
            main_frame,
            text="Job Match - Avaliação de Currículos",
            font=('Segoe UI', 16, 'bold')
        )
        header_label.grid(row=0, column=0, pady=(0, 20))
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 9)
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)

