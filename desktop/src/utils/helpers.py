"""
Helper utility functions
"""

import os
from pathlib import Path


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent


def ensure_directory(path):
    """Ensure a directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)
    return path


def center_window(window, width=None, height=None):
    """
    Center a window on the screen
    
    Args:
        window: The tkinter window to center
        width: Window width (if None, uses current window width)
        height: Window height (if None, uses current window height)
    """
    window.update_idletasks()
    
    if width is None or height is None:
        width = window.winfo_width()
        height = window.winfo_height()
    
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Set window position
    window.geometry(f'{width}x{height}+{x}+{y}')

