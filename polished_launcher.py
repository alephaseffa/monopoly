#!/usr/bin/env python3
"""
@author: Aleph Aseffa
Monopoly Polished Version Launcher

Launch the professionally redesigned Monopoly game with authentic
board design and polished UI components.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def launch_polished_monopoly():
    """Launch the polished Monopoly GUI"""
    try:
        from gui.polished_monopoly_gui import PolishedMonopolyGUI
        
        # Create and run the application
        app = PolishedMonopolyGUI()
        app.run()
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("\nMake sure all required files are present:")
        print("  - gui/polished_monopoly_gui.py")
        print("  - gui/authentic_board.py")
        print("  - gui/polished_panels.py")
        print("  - gui/colors.py")
        print("  - gui/game_controller.py")
        
        # Try to show error in GUI
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch Monopoly:\n{e}\n\n"
                "Please ensure all game files are present."
            )
        except:
            pass
        
        sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        
        # Try to show error in GUI
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Launch Error",
                f"An unexpected error occurred:\n{e}"
            )
        except:
            pass
        
        sys.exit(1)

def main():
    """Main entry point"""
    print("=" * 60)
    print("MONOPOLY - POLISHED EDITION")
    print("Property Trading Game")
    print("=" * 60)
    print("\nLaunching polished Monopoly GUI...")
    
    # Check dependencies
    if not check_dependencies():
        print("Error: tkinter is not available.")
        print("Please install tkinter to run this game.")
        sys.exit(1)
    
    # Launch the game
    launch_polished_monopoly()

if __name__ == "__main__":
    main()