#!/usr/bin/env python3
"""
@author: Aleph Aseffa
GUI Launcher for Monopoly Game

Entry point script that starts the Monopoly GUI application.
Place this in the main project directory for easy launching.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.monopoly_gui import main
    
    if __name__ == "__main__":
        print("Starting Monopoly GUI...")
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all GUI components are properly installed.")
    sys.exit(1)
except Exception as e:
    print(f"Error starting GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)