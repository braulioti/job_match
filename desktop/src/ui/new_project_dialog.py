"""
New Project Dialog
Dialog for creating a new project
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.helpers import center_window
from src.database.db import Database


class NewProjectDialog:
    """Dialog for creating a new project"""
    
    def __init__(self, parent, on_project_created):
        """
        Initialize the dialog
        
        Args:
            parent: Parent window
            on_project_created: Callback function called when project is created
                                Receives (project_id, name, description) as arguments
        """
        self.parent = parent
        self.on_project_created = on_project_created
        self.dialog = None
        self._create_dialog()
    
    def _create_dialog(self):
        """Create and show the dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Cadastrar Novo Projeto")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        
        # Make window modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Project name
        name_label = ttk.Label(main_frame, text="Nome do Projeto:", font=('Segoe UI', 10))
        name_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        name_entry = ttk.Entry(main_frame, width=50, font=('Segoe UI', 10))
        name_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        name_entry.focus()
        
        # Project description
        desc_label = ttk.Label(main_frame, text="Descrição:", font=('Segoe UI', 10))
        desc_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        desc_text = tk.Text(main_frame, width=50, height=6, font=('Segoe UI', 10), wrap=tk.WORD)
        desc_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, sticky=tk.E, pady=(10, 0))
        
        def on_ok():
            """Handle OK button click"""
            name = name_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            # Validate
            if not name:
                messagebox.showerror("Erro", "O nome do projeto é obrigatório.", parent=self.dialog)
                name_entry.focus()
                return
            
            # Insert into database
            try:
                db = Database()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO project (name, description) VALUES (?, ?)",
                    (name, description if description else None)
                )
                project_id = cursor.lastrowid
                conn.commit()
                db.close()
                
                # Call callback with project information
                if self.on_project_created:
                    self.on_project_created(project_id, name, description if description else "")
                
                self.dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar projeto:\n{str(e)}", parent=self.dialog)
        
        def on_cancel():
            """Handle Cancel button click"""
            self.dialog.destroy()
        
        ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=on_cancel)
        cancel_button.pack(side=tk.LEFT)
        
        # Bind Enter key to OK
        self.dialog.bind('<Return>', lambda e: on_ok())
        self.dialog.bind('<Escape>', lambda e: on_cancel())
        
        # Center the window after widgets are created
        self.dialog.update_idletasks()
        center_window(self.dialog, 500, 300)
