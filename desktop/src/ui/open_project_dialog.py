"""
Open Project Dialog
Dialog for selecting and opening an existing project
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.helpers import center_window
from src.entities.project import Project


class OpenProjectDialog:
    """Dialog for opening an existing project"""
    
    def __init__(self, parent, on_project_selected):
        """
        Initialize the dialog
        
        Args:
            parent: Parent window
            on_project_selected: Callback function called when project is selected
                                Receives (project_id, name, description) as arguments
        """
        self.parent = parent
        self.on_project_selected = on_project_selected
        self.dialog = None
        self.projects_listbox = None
        self.projects = []
        self._create_dialog()
    
    def _load_projects(self):
        """Load projects from database in alphabetical order"""
        try:
            projects = Project.get_all(order_by="name ASC")
            
            self.projects = []
            for project in projects:
                self.projects.append({
                    'id': project.id,
                    'name': project.name,
                    'description': project.description if project.description else ''
                })
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar projetos:\n{str(e)}", parent=self.dialog)
            return False
    
    def _create_dialog(self):
        """Create and show the dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Abrir Projeto")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make window modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label
        label = ttk.Label(main_frame, text="Selecione um projeto:", font=('Segoe UI', 10))
        label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Listbox frame with scrollbar
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.projects_listbox = tk.Listbox(
            listbox_frame,
            font=('Segoe UI', 10),
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.projects_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.projects_listbox.yview)
        
        # Bind double-click to OK
        self.projects_listbox.bind('<Double-Button-1>', lambda e: self._on_ok())
        
        # Load projects
        if self._load_projects():
            for project in self.projects:
                self.projects_listbox.insert(tk.END, project['name'])
            
            # Select first item if available
            if self.projects:
                self.projects_listbox.selection_set(0)
                self.projects_listbox.activate(0)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=tk.E, pady=(10, 0))
        
        def on_ok():
            """Handle OK button click"""
            selection = self.projects_listbox.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Por favor, selecione um projeto.", parent=self.dialog)
                return
            
            selected_index = selection[0]
            selected_project = self.projects[selected_index]
            
            # Call callback with project information
            if self.on_project_selected:
                self.on_project_selected(
                    selected_project['id'],
                    selected_project['name'],
                    selected_project['description']
                )
            
            self.dialog.destroy()
        
        def on_cancel():
            """Handle Cancel button click"""
            self.dialog.destroy()
        
        ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=on_cancel)
        cancel_button.pack(side=tk.LEFT)
        
        # Store methods for key bindings
        self._on_ok = on_ok
        self._on_cancel = on_cancel
        
        # Bind Enter key to OK
        self.dialog.bind('<Return>', lambda e: on_ok())
        self.dialog.bind('<Escape>', lambda e: on_cancel())
        
        # Focus on listbox
        self.projects_listbox.focus_set()
        
        # Center the window after widgets are created
        self.dialog.update_idletasks()
        center_window(self.dialog, 500, 400)


