"""
Main Window UI Component
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.ui.new_project_dialog import NewProjectDialog
from src.ui.open_project_dialog import OpenProjectDialog
from src.ui.about_dialog import AboutDialog
from src.ui.configuration_dialog import ConfigurationDialog
from src.ui.builders.main_menu import MainMenuBuilder
from src.config.settings import Settings


class MainWindow:
    """Main window of the application"""
    
    def __init__(self, parent, server_manager=None, config_manager=None, selected_server=None, on_server_changed=None):
        """
        Initialize the main window
        
        Args:
            parent: Parent window
            server_manager: ServerManager instance
            config_manager: ConfigManager instance
            selected_server: Currently selected server
            on_server_changed: Callback function when server is changed
        """
        self.parent = parent
        self.selected_project_id = None  # Global variable to store selected project ID
        self.server_manager = server_manager
        self.config_manager = config_manager
        self.selected_server = selected_server
        self.on_server_changed = on_server_changed
        self._create_menu()
        self._create_widgets()
    
    def _create_menu(self):
        """Create the menu bar using MainMenuBuilder"""
        menu_builder = MainMenuBuilder(
            parent=self.parent,
            on_new_project=self._show_new_project_dialog,
            on_open_project=self._show_open_project_dialog,
            on_exit=self._on_exit,
            on_about=self._show_about,
            on_settings=self._show_configuration_dialog
        )
        menu_builder.build()
    
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
    
    def _show_open_project_dialog(self):
        """Show dialog to open an existing project"""
        def on_project_selected(project_id, name, description):
            """Callback when project is selected"""
            # Store project ID globally
            self.selected_project_id = project_id
            
            # Update UI with project information
            self._update_selected_project(name, description)
        
        OpenProjectDialog(self.parent, on_project_selected)
    
    def _show_about(self):
        """Show about dialog"""
        AboutDialog(self.parent)
    
    def _show_configuration_dialog(self):
        """Show configuration dialog"""
        ConfigurationDialog(
            self.parent,
            self.server_manager,
            self.config_manager,
            self.selected_server,
            self.on_server_changed
        )
    
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
        
        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Logo
        logo_path = Settings.get_logo_path()
        if logo_path.exists():
            try:
                img = Image.open(str(logo_path))
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(
                    header_frame,
                    image=self.logo_photo,
                    bg='#f0f0f0'
                )
                logo_label.grid(row=0, column=0, pady=(0, 5))
            except Exception as e:
                # Fallback to text if image fails to load
                header_label = tk.Label(
                    header_frame,
                    text="Job Match - Avaliação de Currículos",
                    font=('Segoe UI', 16, 'bold'),
                    anchor=tk.CENTER,
                    bg='#f0f0f0'
                )
                header_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
                print(f"Erro ao carregar logo: {e}")
        else:
            # Fallback to text if logo file doesn't exist
            header_label = tk.Label(
                header_frame,
            text="Job Match - Avaliação de Currículos",
                font=('Segoe UI', 16, 'bold'),
                anchor=tk.CENTER,
                bg='#f0f0f0'
            )
            header_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Avaliação de Currículos",
            font=('Segoe UI', 16, 'bold')
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 0))
        
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
        self.project_name_value.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Project description label
        self.project_desc_label = ttk.Label(
            project_info_frame,
            text="Descrição: ",
            font=('Segoe UI', 10, 'bold')
        )
        self.project_desc_label.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(5, 0))
        
        self.project_desc_value = ttk.Label(
            project_info_frame,
            text="",
            font=('Segoe UI', 10),
            wraplength=1  # Will be updated dynamically
        )
        self.project_desc_value.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        # Bind to window resize to update wraplength
        self.parent.bind('<Configure>', self._on_window_resize)
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#f0f0f0'
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
    
    def update_server_status(self, message, is_online):
        """
        Update the server status in the status bar
        
        Args:
            message: Status message to display
            is_online: True if server is online, False otherwise
        """
        if is_online:
            self.status_label.config(
                text=message,
                font=('Segoe UI', 9, 'bold'),
                fg='#2e7d32'  # Green color
            )
        else:
            self.status_label.config(
                text=message,
                font=('Segoe UI', 9, 'bold'),
                fg='#c62828'  # Red color
            )
    
    def _on_window_resize(self, event=None):
        """Handle window resize to update wraplength"""
        if event and event.widget == self.parent:
            # Update wraplength based on window width
            # Account for padding, label width, and margins
            window_width = self.parent.winfo_width()
            if window_width > 1:  # Avoid initial sizing issues
                # Calculate available width: window width - padding - label width - margins
                available_width = window_width - 40 - 150 - 20  # Approximate
                if available_width > 0:
                    self.project_desc_value.config(wraplength=available_width)
    
    def _update_selected_project(self, name, description):
        """Update the selected project information display"""
        self.project_name_value.config(text=name)
        self.project_desc_value.config(text=description if description else "")
        # Update wraplength after setting text
        self._on_window_resize()

