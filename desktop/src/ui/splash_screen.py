"""
Splash Screen
Shows application loading progress
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.config.settings import Settings
from src.utils.helpers import center_window


class SplashScreen:
    """Splash screen with progress bar"""
    
    def __init__(self, parent):
        """
        Initialize the splash screen
        
        Args:
            parent: Parent window (tk.Tk)
        """
        self.parent = parent
        self.splash = None
        self.progress_var = None
        self.status_var = None
        self._create_splash()
    
    def _create_splash(self):
        """Create and show the splash screen"""
        # Get screen dimensions from parent first
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Fixed window dimensions
        width = 500
        height = 400
        
        # Calculate center position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Create splash window
        self.splash = tk.Toplevel(self.parent)
        self.splash.title("Job Match")
        self.splash.resizable(False, False)
        
        # Configure background
        self.splash.configure(bg='#ffffff')
        
        # Set geometry with size and position BEFORE overrideredirect
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Force update to ensure geometry is applied
        self.splash.update_idletasks()
        
        # Re-apply geometry after overrideredirect to ensure position is correct
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.update()
        
        # Main frame
        main_frame = tk.Frame(self.splash, bg='#ffffff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo
        logo_path = Settings.get_logo_path()
        if logo_path.exists():
            try:
                img = Image.open(str(logo_path))
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(
                    main_frame,
                    image=self.logo_photo,
                    bg='#ffffff'
                )
                logo_label.pack(pady=(0, 20))
            except Exception as e:
                print(f"Erro ao carregar logo na splash: {e}")
                # Fallback to text
                title_label = tk.Label(
                    main_frame,
                    text="Job Match",
                    font=('Segoe UI', 24, 'bold'),
                    bg='#ffffff',
                    fg='#333333'
                )
                title_label.pack(pady=(0, 20))
        else:
            # Fallback to text if logo doesn't exist
            title_label = tk.Label(
                main_frame,
                text="Job Match",
                font=('Segoe UI', 24, 'bold'),
                bg='#ffffff',
                fg='#333333'
            )
            title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Avaliação de Currículos",
            font=('Segoe UI', 14),
            bg='#ffffff',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Status label
        self.status_var = tk.StringVar(value="Inicializando...")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#333333'
        )
        status_label.pack(pady=(0, 10))
        
        # Progress bar frame
        progress_frame = tk.Frame(main_frame, bg='#ffffff')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack()
        
        # Version label
        version_label = tk.Label(
            main_frame,
            text=f"Versão {Settings.APP_VERSION}",
            font=('Segoe UI', 8),
            bg='#ffffff',
            fg='#999999'
        )
        version_label.pack(side=tk.BOTTOM, pady=(20, 0))
        
        # Force update to render all widgets
        self.splash.update_idletasks()
        
        # Re-center the window after widgets are rendered (in case size changed)
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        width = 500
        height = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Use wm_geometry for more reliable positioning with overrideredirect
        self.splash.wm_geometry(f"{width}x{height}+{x}+{y}")
        
        # Also set geometry as backup
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make sure splash is on top and visible
        self.splash.lift()
        self.splash.attributes('-topmost', True)
        
        # Final update to ensure window is visible and centered
        self.splash.update_idletasks()
        self.splash.update()
    
    def update_progress(self, value, status_text=None):
        """
        Update progress bar and status text
        
        Args:
            value: Progress value (0-100)
            status_text: Optional status text to display
        """
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        
        self.progress_var.set(value)
        
        if status_text:
            self.status_var.set(status_text)
        
        self.splash.update_idletasks()
    
    def close(self):
        """Close the splash screen"""
        if self.splash:
            self.splash.destroy()
            self.splash = None


