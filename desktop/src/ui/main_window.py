"""
Main Window UI Component
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.ui.new_project_dialog import NewProjectDialog
from src.ui.open_project_dialog import OpenProjectDialog
from src.ui.new_vacancy_dialog import NewVacancyDialog
from src.ui.about_dialog import AboutDialog
from src.ui.configuration_dialog import ConfigurationDialog
from src.ui.builders.main_menu import MainMenuBuilder
from src.config.settings import Settings
from src.entities.job_vacancy import JobVacancy


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
        self.project_info_frame = ttk.Frame(main_frame)
        self.project_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        self.project_info_frame.columnconfigure(1, weight=1)
        
        # Project name label
        self.project_name_label = ttk.Label(
            self.project_info_frame,
            text="Projeto Selecionado: ",
            font=('Segoe UI', 10, 'bold')
        )
        self.project_name_label.grid(row=0, column=0, sticky=tk.W)
        
        self.project_name_value = ttk.Label(
            self.project_info_frame,
            text="",
            font=('Segoe UI', 10)
        )
        self.project_name_value.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Project description label
        self.project_desc_label = ttk.Label(
            self.project_info_frame,
            text="Descrição: ",
            font=('Segoe UI', 10, 'bold')
        )
        self.project_desc_label.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(5, 0))
        
        self.project_desc_value = ttk.Label(
            self.project_info_frame,
            text="",
            font=('Segoe UI', 10),
            wraplength=1  # Will be updated dynamically
        )
        self.project_desc_value.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        # Initially hide project info frame (no project selected)
        self.project_info_frame.grid_remove()
        
        # Bind to window resize to update wraplength
        self.parent.bind('<Configure>', self._on_window_resize)
        
        # Content area panel (below description)
        self.content_panel = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        self.content_panel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        self.content_panel.columnconfigure(0, weight=1)
        self.content_panel.rowconfigure(0, weight=1)
        
        # PanedWindow for splitter between left and right panels
        self.paned_window = ttk.PanedWindow(self.content_panel, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind to sash movement to update wraplength
        def on_sash_moved(event):
            """Handle splitter movement"""
            self.parent.after(50, self._update_vacancy_cards_wraplength)
        
        self.paned_window.bind('<ButtonRelease-1>', on_sash_moved)
        
        # Left panel (15% of width)
        self.left_panel = ttk.Frame(self.paned_window, relief=tk.SUNKEN, borderwidth=1)
        self.paned_window.add(self.left_panel, weight=1)
        
        # Configure left panel grid
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(1, weight=1)
        
        # Toolbar in left panel
        toolbar_frame = ttk.Frame(self.left_panel)
        toolbar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        toolbar_frame.columnconfigure(0, weight=1)
        
        # Add Vacancy button
        add_vacancy_button = ttk.Button(
            toolbar_frame,
            text="Adicionar Vaga",
            command=self._on_add_vacancy
        )
        add_vacancy_button.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Scrollable panel below toolbar (100% of remaining area)
        scrollable_frame = ttk.Frame(self.left_panel)
        scrollable_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=(0, 5))
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Canvas for scrolling
        self.vacancies_canvas = tk.Canvas(
            scrollable_frame,
            yscrollcommand=scrollbar.set,
            bg='#f0f0f0',
            highlightthickness=0
        )
        self.vacancies_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.vacancies_canvas.yview)
        
        # Inner frame for content
        self.vacancies_content_frame = ttk.Frame(self.vacancies_canvas)
        self.vacancies_content_frame.columnconfigure(0, weight=1)
        self.vacancies_canvas_window = self.vacancies_canvas.create_window((0, 0), window=self.vacancies_content_frame, anchor=tk.NW)
        
        # Configure canvas scrolling
        def configure_scroll_region(event=None):
            self.vacancies_canvas.configure(scrollregion=self.vacancies_canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas_width = event.width
            self.vacancies_canvas.itemconfig(self.vacancies_canvas_window, width=canvas_width)
            # Update wraplength for existing vacancy cards
            self._update_vacancy_cards_wraplength()
        
        self.vacancies_content_frame.bind('<Configure>', configure_scroll_region)
        self.vacancies_canvas.bind('<Configure>', configure_canvas_width)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            self.vacancies_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.vacancies_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Right panel (85% of width)
        self.right_panel = ttk.Frame(self.paned_window, relief=tk.SUNKEN, borderwidth=1)
        self.paned_window.add(self.right_panel, weight=5)
        
        # Configure right panel grid
        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=1)  # Scrollable area takes available space
        # row 1 will be for progress bar (no weight, just takes needed space)
        
        # Scrollable panel (100% width and height, resizable with splitter)
        right_scrollable_frame = ttk.Frame(self.right_panel)
        right_scrollable_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=(5, 0))
        right_scrollable_frame.columnconfigure(0, weight=1)
        right_scrollable_frame.rowconfigure(0, weight=1)
        
        # Scrollbar (vertical)
        right_scrollbar = ttk.Scrollbar(right_scrollable_frame, orient=tk.VERTICAL)
        right_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Canvas for scrolling
        self.right_canvas = tk.Canvas(
            right_scrollable_frame,
            yscrollcommand=right_scrollbar.set,
            bg='#f0f0f0',
            highlightthickness=0
        )
        self.right_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_scrollbar.config(command=self.right_canvas.yview)
        
        # Inner frame for content
        self.right_content_frame = ttk.Frame(self.right_canvas)
        self.right_canvas_window = self.right_canvas.create_window((0, 0), window=self.right_content_frame, anchor=tk.NW)
        
        # Configure canvas scrolling
        def configure_right_scroll_region(event=None):
            self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))
        
        def configure_right_canvas_width(event):
            canvas_width = event.width
            self.right_canvas.itemconfig(self.right_canvas_window, width=canvas_width)
        
        self.right_content_frame.bind('<Configure>', configure_right_scroll_region)
        self.right_canvas.bind('<Configure>', configure_right_canvas_width)
        
        # Mouse wheel scrolling for right panel
        def on_right_mousewheel(event):
            self.right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.right_canvas.bind_all("<MouseWheel>", on_right_mousewheel)
        
        # Progress bar at the bottom, outside the scrollable area (100% width, resizable with splitter)
        progress_frame = ttk.Frame(self.right_panel)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            maximum=100,
            length=100  # Will be resized automatically
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Set initial sizes (15% and 85%)
        # This will be set after the window is shown
        self.parent.after(100, self._set_panel_sizes)
        
        # Initially hide content panel (no project selected)
        self.content_panel.grid_remove()

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
    
    def _set_panel_sizes(self):
        """Set initial panel sizes (15% left, 85% right)"""
        try:
            if self.content_panel.winfo_viewable():
                panel_width = self.content_panel.winfo_width()
                if panel_width > 1:
                    # Calculate 15% of panel width for left panel
                    left_width = int(panel_width * 0.15)
                    # PanedWindow uses sashpos to set the splitter position
                    self.paned_window.sashpos(0, left_width)
        except:
            pass  # Ignore errors during initial sizing
    
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
                
                # Update panel sizes if content panel is visible
                if hasattr(self, 'content_panel') and self.content_panel.winfo_viewable():
                    self.parent.after(50, self._set_panel_sizes)
    
    def _on_add_vacancy(self):
        """Handle Add Vacancy button click"""
        if not self.selected_project_id:
            from tkinter import messagebox
            messagebox.showwarning("Aviso", "Por favor, selecione um projeto primeiro.", parent=self.parent)
            return
        
        def on_vacancy_created(vacancy_id, title, description, resume_folder):
            """Callback when vacancy is created"""
            # Reload vacancies list
            self._load_vacancies()
        
        NewVacancyDialog(self.parent, self.selected_project_id, on_vacancy_created)
    
    def _update_vacancy_cards_wraplength(self):
        """Update wraplength for all vacancy title labels"""
        try:
            # Wait a bit for the canvas to update its size
            self.parent.after(10, self._do_update_wraplength)
        except Exception as e:
            print(f"Erro ao atualizar wraplength: {e}")
    
    def _do_update_wraplength(self):
        """Actually update wraplength for all vacancy title labels"""
        try:
            canvas_width = self.vacancies_canvas.winfo_width()
            if canvas_width > 1:
                # Calculate available width: canvas width - padding - scrollbar width
                scrollbar_width = 20  # Approximate scrollbar width
                available_width = canvas_width - scrollbar_width - 20  # Account for padding
                # Wraplength: available width - prefix label width - padding
                # Prefix "Título da Vaga:" is approximately 120 pixels, plus padding
                wraplength = max(50, available_width - 130)  # Minimum 50 pixels
                
                # Update wraplength for all title value labels
                for card_frame in self.vacancies_content_frame.winfo_children():
                    if isinstance(card_frame, ttk.Frame):
                        for widget in card_frame.winfo_children():
                            if isinstance(widget, ttk.Label):
                                try:
                                    font_tuple = widget.cget('font')
                                    # Check if it's the title value label (not bold)
                                    is_bold = False
                                    if isinstance(font_tuple, tuple):
                                        is_bold = len(font_tuple) > 2 and font_tuple[2] == 'bold'
                                    elif isinstance(font_tuple, str):
                                        is_bold = 'bold' in font_tuple.lower()
                                    
                                    if not is_bold:
                                        widget.config(wraplength=wraplength)
                                        # Force update to recalculate text wrapping
                                        widget.update_idletasks()
                                except Exception as e:
                                    print(f"Erro ao atualizar label: {e}")
                
                # Update scroll region after wraplength changes
                self.vacancies_content_frame.update_idletasks()
                self.vacancies_canvas.configure(scrollregion=self.vacancies_canvas.bbox("all"))
        except Exception as e:
            print(f"Erro ao atualizar wraplength: {e}")
    
    def _load_vacancies(self):
        """Load and display job vacancies for the selected project"""
        # Clear existing cards
        for widget in self.vacancies_content_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_project_id:
            return
        
        try:
            # Get all vacancies for the selected project
            vacancies = JobVacancy.get_by_project_id(self.selected_project_id, order_by="title ASC")
            
            # Get canvas width for wraplength calculation
            canvas_width = self.vacancies_canvas.winfo_width()
            if canvas_width < 1:
                # If canvas not yet rendered, use a default width
                canvas_width = 200
            
            # Calculate available width for text (canvas width - padding - scrollbar)
            available_width = canvas_width - 30  # Account for padding and scrollbar
            wraplength = available_width - 120  # Account for prefix label and padding
            
            # Create cards for each vacancy
            for idx, vacancy in enumerate(vacancies):
                # Card frame
                card_frame = ttk.Frame(
                    self.vacancies_content_frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                card_frame.grid(row=idx, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
                card_frame.columnconfigure(1, weight=1)
                
                # "Título da Vaga:" label (bold)
                title_prefix_label = ttk.Label(
                    card_frame,
                    text="Título da Vaga:",
                    font=('Segoe UI', 9, 'bold'),
                    anchor=tk.W
                )
                title_prefix_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 5), pady=10)
                
                # Title value label (normal, with word wrap)
                title_value_label = ttk.Label(
                    card_frame,
                    text=vacancy.title,
                    font=('Segoe UI', 9),
                    anchor=tk.W,
                    wraplength=wraplength
                )
                title_value_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=10)
            
            # Update scroll region
            self.vacancies_content_frame.update_idletasks()
            self.vacancies_canvas.configure(scrollregion=self.vacancies_canvas.bbox("all"))
        except Exception as e:
            print(f"Erro ao carregar vagas: {e}")
    
    def _update_selected_project(self, name, description):
        """Update the selected project information display"""
        if name:
            # Show project info frame and content panel
            self.project_info_frame.grid()
            self.content_panel.grid()
            self.project_name_value.config(text=name)
            self.project_desc_value.config(text=description if description else "")
            # Update wraplength after setting text
            self._on_window_resize()
            # Load vacancies for the selected project
            self._load_vacancies()
        else:
            # Hide project info frame and content panel if no project selected
            self.project_info_frame.grid_remove()
            self.content_panel.grid_remove()
            # Clear vacancies list
            for widget in self.vacancies_content_frame.winfo_children():
                widget.destroy()

