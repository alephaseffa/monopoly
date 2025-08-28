#!/usr/bin/env python3
"""
Simple launcher for the polished Monopoly GUI
This script avoids import issues by running the GUI directly
"""

import sys
import os

# Add the gui directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gui'))

# Import the polished GUI
from polished_monopoly_gui import PolishedMonopolyGUI

if __name__ == "__main__":
    try:
        app = PolishedMonopolyGUI()
        app.run()
    except Exception as e:
        print(f"Error starting the application: {e}")
        import traceback
        traceback.print_exc()
