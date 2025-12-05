"""
About Dialog
Dialog showing application information
"""

import tkinter as tk
from tkinter import ttk
from src.config.settings import Settings
from src.utils.helpers import center_window


class AboutDialog:
    """Dialog showing application information"""
    
    def __init__(self, parent):
        """
        Initialize the dialog
        
        Args:
            parent: Parent window
        """
        self.parent = parent
        self.about_window = None
        self._create_dialog()
    
    def _create_dialog(self):
        """Create and show the dialog"""
        self.about_window = tk.Toplevel(self.parent)
        self.about_window.title("Sobre")
        self.about_window.geometry("400x300")
        self.about_window.resizable(False, False)
        
        # Make window modal
        self.about_window.transient(self.parent)
        self.about_window.grab_set()
        self.about_window.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(self.about_window, padding="20")
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
            command=self.about_window.destroy
        )
        close_button.pack()
        
        # Bind Enter key to close
        self.about_window.bind('<Return>', lambda e: self.about_window.destroy())
        self.about_window.bind('<Escape>', lambda e: self.about_window.destroy())
        
        # Center the window after widgets are created
        self.about_window.update_idletasks()
        center_window(self.about_window, 400, 300)
