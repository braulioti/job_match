"""
Main Window UI Component
"""

import tkinter as tk
from tkinter import ttk
from src.ui.new_project_dialog import NewProjectDialog
from src.ui.about_dialog import AboutDialog


class MainWindow:
    """Main window of the application"""
    
    def __init__(self, parent):
        """Initialize the main window"""
        self.parent = parent
        self.selected_project_id = None  # Global variable to store selected project ID
        self._create_menu()
        self._create_widgets()
    
    def _create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        # Arquivo menu
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Projeto", menu=arquivo_menu)
        arquivo_menu.add_command(label="Cadastrar Novo Projeto...", command=self._show_new_project_dialog, accelerator="Ctrl+N")
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self._on_exit, accelerator="Ctrl+Q")
        
        # Ajuda menu
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self._show_about)
        
        # Bind keyboard shortcuts
        self.parent.bind('<Control-q>', lambda e: self._on_exit())
        self.parent.bind('<Control-n>', lambda e: self._show_new_project_dialog())
    
    def _on_exit(self):
        """Handle exit menu item"""
        self.parent.quit()
    
    def _show_new_project_dialog(self):
        """Show dialog to create a new project"""
        def on_project_created(project_id, name, description):
            """Callback when project is created"""
            # Store project ID globally
            self.selected_project_id = project_id
            
            # Update UI with project information
            self._update_selected_project(name, description)
        
        NewProjectDialog(self.parent, on_project_created)
    
    def _show_about(self):
        """Show about dialog"""
        AboutDialog(self.parent)
    
    def _create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="Job Match - Avaliação de Currículos",
            font=('Segoe UI', 16, 'bold'),
            anchor=tk.CENTER
        )
        header_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Selected project info frame
        project_info_frame = ttk.Frame(main_frame)
        project_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        project_info_frame.columnconfigure(1, weight=1)
        
        # Project name label
        self.project_name_label = ttk.Label(
            project_info_frame,
            text="Projeto Selecionado: ",
            font=('Segoe UI', 10, 'bold')
        )
        self.project_name_label.grid(row=0, column=0, sticky=tk.W)
        
        self.project_name_value = ttk.Label(
            project_info_frame,
            text="",
            font=('Segoe UI', 10)
        )
        self.project_name_value.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Project description label
        self.project_desc_label = ttk.Label(
            project_info_frame,
            text="Descrição: ",
            font=('Segoe UI', 10, 'bold')
        )
        self.project_desc_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.project_desc_value = ttk.Label(
            project_info_frame,
            text="",
            font=('Segoe UI', 10),
            wraplength=600
        )
        self.project_desc_value.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 9)
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
    
    def _update_selected_project(self, name, description):
        """Update the selected project information display"""
        self.project_name_value.config(text=name)
        self.project_desc_value.config(text=description if description else "")

