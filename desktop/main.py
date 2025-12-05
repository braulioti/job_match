"""
Job Match Desktop Application
Main entry point for the desktop application
"""

import sys
import os
from pathlib import Path

# Add src directory to path (for development)
if __name__ == '__main__':
    base_dir = Path(__file__).parent
    src_dir = base_dir / 'src'
    if src_dir.exists() and str(src_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))

from src.app import JobMatchApp


def main():
    """Main function to start the application"""
    app = JobMatchApp()
    app.run()


if __name__ == '__main__':
    main()

