"""
New Vacancy Dialog
Dialog for creating a new job vacancy
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.utils.helpers import center_window
from src.entities.job_vacancy import JobVacancy


class NewVacancyDialog:
    """Dialog for creating a new job vacancy"""
    
    def __init__(self, parent, project_id, on_vacancy_created):
        """
        Initialize the dialog
        
        Args:
            parent: Parent window
            project_id: Project ID to associate the vacancy with
            on_vacancy_created: Callback function called when vacancy is created
                              Receives (vacancy_id, title, description, resume_folder) as arguments
        """
        self.parent = parent
        self.project_id = project_id
        self.on_vacancy_created = on_vacancy_created
        self.dialog = None
        self.resume_folder_path = None
        self._create_dialog()
    
    def _create_dialog(self):
        """Create and show the dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Adicionar Vaga")
        self.dialog.geometry("600x480")
        self.dialog.resizable(False, False)
        
        # Make window modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Título:", font=('Segoe UI', 10))
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        title_entry = ttk.Entry(main_frame, width=60, font=('Segoe UI', 10))
        title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        title_entry.focus()
        
        # Description
        desc_label = ttk.Label(main_frame, text="Descrição:", font=('Segoe UI', 10))
        desc_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        desc_text = tk.Text(main_frame, width=60, height=8, font=('Segoe UI', 10), wrap=tk.WORD)
        desc_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Resume folder selection
        folder_label = ttk.Label(main_frame, text="Pasta de Currículos:", font=('Segoe UI', 10))
        folder_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_path_var = tk.StringVar(value="")
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=50, font=('Segoe UI', 10), state='readonly')
        folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        def browse_folder():
            """Open folder selection dialog"""
            folder = filedialog.askdirectory(
                title="Selecione a pasta de currículos",
                parent=self.dialog
            )
            if folder:
                self.resume_folder_path = folder
                self.folder_path_var.set(folder)
        
        browse_button = ttk.Button(folder_frame, text="Procurar...", command=browse_folder)
        browse_button.grid(row=0, column=1, sticky=tk.W)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        folder_frame.columnconfigure(0, weight=1)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, sticky=tk.E, pady=(20, 0))
        
        def on_ok():
            """Handle OK button click"""
            title = title_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            resume_folder = self.resume_folder_path if self.resume_folder_path else None
            
            # Validate
            if not title:
                messagebox.showerror("Erro", "O título da vaga é obrigatório.", parent=self.dialog)
                title_entry.focus()
                return
            
            # Insert into database
            try:
                vacancy = JobVacancy.create(
                    project_id=self.project_id,
                    title=title,
                    description=description if description else None,
                    resume_folder=resume_folder
                )
                
                # Call callback with vacancy information
                if self.on_vacancy_created:
                    self.on_vacancy_created(
                        vacancy.id,
                        vacancy.title,
                        vacancy.description if vacancy.description else "",
                        vacancy.resume_folder if vacancy.resume_folder else ""
                    )
                
                self.dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar vaga:\n{str(e)}", parent=self.dialog)
        
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
        center_window(self.dialog, 600, 480)

