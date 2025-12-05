"""
Main Menu Builder
Responsible for building the main application menu
"""

import tkinter as tk


class MainMenuBuilder:
    """Builder class for creating the main application menu"""
    
    def __init__(self, parent, on_new_project=None, on_open_project=None, on_exit=None, on_about=None, on_settings=None):
        """
        Initialize the menu builder
        
        Args:
            parent: Parent window (tk.Tk or tk.Toplevel)
            on_new_project: Callback function for "Cadastrar Novo Projeto" menu item
            on_open_project: Callback function for "Abrir Projeto" menu item
            on_exit: Callback function for "Sair" menu item
            on_about: Callback function for "Sobre" menu item
            on_settings: Callback function for "Configurações" menu item
        """
        self.parent = parent
        self.on_new_project = on_new_project
        self.on_open_project = on_open_project
        self.on_exit = on_exit
        self.on_about = on_about
        self.on_settings = on_settings
        self.menubar = None
    
    def build(self):
        """
        Build and configure the menu bar
        
        Returns:
            tk.Menu: The created menubar
        """
        self.menubar = tk.Menu(self.parent)
        self.parent.config(menu=self.menubar)
        
        # Build Projeto menu
        self._build_projeto_menu()
        
        # Build Ferramentas menu
        self._build_ferramentas_menu()
        
        # Build Ajuda menu
        self._build_ajuda_menu()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
        
        return self.menubar
    
    def _build_projeto_menu(self):
        """Build the Projeto menu"""
        arquivo_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Projeto", menu=arquivo_menu)
        
        # Cadastrar Novo Projeto
        arquivo_menu.add_command(
            label="Cadastrar Novo Projeto...",
            command=self._handle_new_project,
            accelerator="Ctrl+N"
        )
        
        # Abrir Projeto
        arquivo_menu.add_command(
            label="Abrir Projeto...",
            command=self._handle_open_project,
            accelerator="Ctrl+A"
        )
        
        arquivo_menu.add_separator()
        
        # Sair
        arquivo_menu.add_command(
            label="Sair",
            command=self._handle_exit,
            accelerator="Ctrl+Q"
        )
    
    def _build_ferramentas_menu(self):
        """Build the Ferramentas menu"""
        ferramentas_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ferramentas", menu=ferramentas_menu)
        
        # Configurações
        ferramentas_menu.add_command(
            label="Configurações...",
            command=self._handle_settings
        )
    
    def _build_ajuda_menu(self):
        """Build the Ajuda menu"""
        ajuda_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        
        # Sobre
        ajuda_menu.add_command(
            label="Sobre",
            command=self._handle_about
        )
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.parent.bind('<Control-q>', lambda e: self._handle_exit())
        self.parent.bind('<Control-n>', lambda e: self._handle_new_project())
        self.parent.bind('<Control-a>', lambda e: self._handle_open_project())
    
    def _handle_new_project(self):
        """Handle new project menu item click"""
        if self.on_new_project:
            self.on_new_project()
    
    def _handle_open_project(self):
        """Handle open project menu item click"""
        if self.on_open_project:
            self.on_open_project()
    
    def _handle_exit(self):
        """Handle exit menu item click"""
        if self.on_exit:
            self.on_exit()
    
    def _handle_settings(self):
        """Handle settings menu item click"""
        if self.on_settings:
            self.on_settings()
    
    def _handle_about(self):
        """Handle about menu item click"""
        if self.on_about:
            self.on_about()
