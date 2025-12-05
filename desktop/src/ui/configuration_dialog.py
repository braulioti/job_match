"""
Configuration Dialog
Dialog for application settings
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from src.utils.helpers import center_window
from src.interfaces.server import ServerInterface


class ConfigurationDialog:
    """Dialog for configuring application settings"""
    
    def __init__(self, parent, server_manager, config_manager, selected_server, on_server_changed=None):
        """
        Initialize the configuration dialog
        
        Args:
            parent: Parent window
            server_manager: ServerManager instance
            config_manager: ConfigManager instance
            selected_server: Currently selected server (ServerInterface or None)
            on_server_changed: Callback function called when server is changed (receives new ServerInterface)
        """
        self.parent = parent
        self.server_manager = server_manager
        self.config_manager = config_manager
        self.selected_server = selected_server
        self.on_server_changed = on_server_changed
        self.dialog = None
        self.server_combo = None
        self.server_values = []
        self._create_dialog()
    
    def _create_dialog(self):
        """Create and show the dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Configurações")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make window modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.focus_set()
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Server selection frame
        server_frame = ttk.LabelFrame(main_frame, text="Servidor do Projeto", padding="10")
        server_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Server label
        server_label = ttk.Label(server_frame, text="Servidor:")
        server_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Server combo
        self.server_combo = ttk.Combobox(server_frame, state="readonly", width=40)
        self.server_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Load servers into combo
        self._load_servers()
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        def on_ok():
            """Handle OK button click"""
            selected_index = self.server_combo.current()
            if selected_index >= 0 and selected_index < len(self.server_values):
                new_server = self.server_values[selected_index]
                
                # Update config.ini
                self.config_manager.set('Server', 'url', new_server['url'])
                self.config_manager.save()
                
                # Notify callback if provided
                if self.on_server_changed:
                    self.on_server_changed(new_server)
            
            self.dialog.destroy()
        
        def on_cancel():
            """Handle Cancel button click"""
            self.dialog.destroy()
        
        ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
        ok_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT)
        
        # Center the window after widgets are created
        self.dialog.update_idletasks()
        center_window(self.dialog, 500, 400)
    
    def _load_servers(self):
        """Load servers into the combo box"""
        servers = self.server_manager.servers
        self.server_values = servers
        
        # Create display names for combo (name - url)
        display_names = [f"{server['name']} - {server['url']}" for server in servers]
        self.server_combo['values'] = display_names
        
        # Set selected server
        if self.selected_server:
            try:
                selected_index = next(
                    i for i, server in enumerate(servers) 
                    if server['url'] == self.selected_server['url']
                )
                self.server_combo.current(selected_index)
            except StopIteration:
                # Server not found in list, select first if available
                if servers:
                    self.server_combo.current(0)
        elif servers:
            # No server selected, select first
            self.server_combo.current(0)
