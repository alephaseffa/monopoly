"""
Monopoly GUI Package

A complete graphical user interface for the Monopoly board game,
featuring a colorful game board, player management, and game controls.
"""

__version__ = "1.0.0"
__author__ = "Aleph Aseffa"

# Import main components for easier access
from .monopoly_gui import MonopolyGUI
from .game_controller import GameController
from .board_canvas import BoardCanvas
from .colors import *

__all__ = [
    'MonopolyGUI',
    'GameController', 
    'BoardCanvas',
    'PROPERTY_COLORS',
    'UI_COLORS',
    'SIZES',
    'FONTS'
]