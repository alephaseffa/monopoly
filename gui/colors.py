"""
@author: Aleph Aseffa
Monopoly Authentic Color Scheme and Visual Design System

Contains the official Monopoly colors, fonts, and comprehensive design tokens
following the classic Hasbro Monopoly board game aesthetics.
"""

# ========================================================================
# AUTHENTIC MONOPOLY PROPERTY GROUP COLORS
# Based on official Hasbro Monopoly color specifications
# ========================================================================

PROPERTY_COLORS = {
    # Standard Property Groups
    "Brown": "#955436",        # Mediterranean/Baltic - Dark Brown
    "Light Blue": "#AAE0FA",   # Oriental/Vermont/Connecticut - Light Blue  
    "Pink": "#D93A96",         # St. Charles/States/Virginia - Magenta/Pink
    "Orange": "#F7941D",       # St. James/Tennessee/New York - Orange
    "Red": "#ED1B24",          # Kentucky/Indiana/Illinois - Red
    "Yellow": "#FEF200",       # Atlantic/Ventnor/Marvin Gardens - Yellow
    "Green": "#1FB25A",        # Pacific/North Carolina/Pennsylvania - Green
    "Blue": "#0072BB",         # Park Place/Boardwalk - Dark Blue
    
    # Special Property Types
    "Railroad": "#000000",     # Black for all railroads
    "Utilities": "#E7E7E7",    # Light gray for utilities
}

# ========================================================================
# MONOPOLY BOARD THEME COLORS
# ========================================================================

BOARD_COLORS = {
    # Board Background and Surface
    "board_center": "#C8E6C9",      # Classic Monopoly light green center
    "board_edge": "#2C5F2D",        # Dark green board border
    "board_surface": "#FDFDF4",     # Cream/off-white property spaces
    
    # Corner Spaces
    "go_background": "#ED1B24",     # Red GO arrow background
    "go_text": "#FFFFFF",           # White GO text
    "jail_background": "#FF8C00",   # Orange jail space
    "jail_bars": "#000000",         # Black jail bars
    "parking_background": "#FFFFFF", # White free parking
    "parking_text": "#ED1B24",      # Red free parking text
    "go_to_jail_bg": "#FF0000",     # Red go to jail background
    
    # Special Spaces
    "chance_background": "#FF8C00",      # Orange chance spaces
    "chance_text": "#000000",            # Black chance text
    "community_chest_bg": "#87CEEB",     # Sky blue community chest
    "community_chest_text": "#000000",   # Black community chest text
    "tax_background": "#FFFFFF",         # White tax spaces
    "tax_text": "#000000",               # Black tax text
    
    # Property Elements
    "property_header": "#000000",        # Black property name bars
    "property_text": "#000000",          # Black property text
    "property_border": "#000000",        # Black borders
    "property_price_bg": "#FFFFFF",      # White price background
}

# ========================================================================
# UI THEME COLORS
# Polished, professional interface colors
# ========================================================================

UI_COLORS = {
    # Main Application
    "app_background": "#F5F5F0",          # Warm off-white background
    "panel_background": "#FFFFFF",        # Clean white panels
    "panel_border": "#D4D4D4",           # Subtle gray borders
    "panel_shadow": "#00000010",         # Subtle shadow color
    
    # Typography
    "text_primary": "#212121",           # Near black for main text
    "text_secondary": "#757575",         # Medium gray for secondary
    "text_tertiary": "#9E9E9E",          # Light gray for hints
    "text_accent": "#ED1B24",            # Monopoly red for emphasis
    "text_success": "#1FB25A",           # Green for positive
    "text_warning": "#F7941D",           # Orange for warnings
    "text_error": "#ED1B24",             # Red for errors
    "text_info": "#0072BB",              # Blue for information
    
    # Interactive Elements
    "button_primary": "#ED1B24",         # Monopoly red primary buttons
    "button_primary_hover": "#C41E1E",   # Darker red on hover
    "button_primary_active": "#A01818",  # Even darker on click
    "button_secondary": "#1FB25A",       # Green secondary buttons
    "button_secondary_hover": "#18904A", # Darker green on hover
    "button_warning": "#F7941D",         # Orange warning buttons
    "button_disabled": "#E0E0E0",        # Light gray disabled
    "button_text": "#FFFFFF",            # White button text
    "button_disabled_text": "#9E9E9E",   # Gray disabled text
    
    # Player Colors - Vibrant, distinct colors
    "player_colors": [
        "#ED1B24",    # Classic Red
        "#0072BB",    # Classic Blue  
        "#1FB25A",    # Classic Green
        "#FEF200",    # Classic Yellow
        "#F7941D",    # Classic Orange
        "#D93A96",    # Classic Pink
        "#955436",    # Classic Brown
        "#9B59B6"     # Purple (additional)
    ],
    
    # Game Elements
    "dice_background": "#FFFFFF",        # White dice background
    "dice_dots": "#000000",              # Black dice dots
    "dice_border": "#000000",            # Black dice border
    "token_glow": "#FFD700",            # Gold glow for current player
    "property_highlight": "#FFD70080",   # Semi-transparent gold highlight
    "property_owned": "#4CAF5040",       # Semi-transparent green for owned
    "property_mortgaged": "#ED1B2440",   # Semi-transparent red for mortgaged
}

# ========================================================================
# SIZE SPECIFICATIONS
# Based on classic Monopoly board proportions
# ========================================================================

SIZES = {
    # Window and Layout
    "window_width": 1400,              # Wider for better layout
    "window_height": 900,              # Standard height
    "board_size": 800,                # Larger board for better visibility
    "board_padding": 20,               # Padding around board
    
    # Board Spaces
    "corner_size": 110,               # Corner square size
    "property_width": 63,              # Property space width  
    "property_height": 90,             # Property space height
    "property_color_bar": 20,         # Color bar height on properties
    
    # UI Panels
    "side_panel_width": 320,          # Right side panel width
    "player_card_height": 80,         # Player info card height
    "button_height": 40,              # Standard button height
    "panel_spacing": 12,              # Space between panels
    
    # Game Elements
    "token_size": 20,                 # Player token diameter
    "token_border": 2,                # Token border width
    "dice_size": 50,                  # Individual die size
    "dice_spacing": 10,               # Space between dice
    "house_size": 12,                 # House width/height
    "hotel_width": 16,                # Hotel width
    "hotel_height": 14,               # Hotel height
}

# ========================================================================
# TYPOGRAPHY
# Classic Monopoly-inspired fonts
# ========================================================================

FONTS = {
    # Headers and Titles
    "title_large": ("Helvetica", 24, "bold"),      # Main title
    "title_medium": ("Helvetica", 18, "bold"),     # Section titles
    "title_small": ("Helvetica", 14, "bold"),      # Sub-section titles
    
    # Board Text
    "property_name": ("Arial", 8, "bold"),         # Property names on board
    "property_price": ("Arial", 7, "normal"),      # Property prices
    "corner_text": ("Helvetica", 11, "bold"),      # Corner space text
    "special_space": ("Arial", 9, "bold"),         # Chance/Community chest
    
    # UI Text
    "player_name": ("Helvetica", 13, "bold"),      # Player names
    "player_info": ("Arial", 11, "normal"),        # Player stats
    "button_text": ("Helvetica", 11, "bold"),      # Button labels
    "status_text": ("Arial", 10, "normal"),        # Status messages
    "log_text": ("Consolas", 9, "normal"),         # Game log entries
    
    # Special Elements
    "dice_number": ("Helvetica", 20, "bold"),      # Dice result display
    "money_amount": ("Arial", 12, "bold"),         # Money displays
    "property_deed": ("Times New Roman", 10, "normal"), # Property card text
}

# ========================================================================
# ANIMATION AND EFFECTS
# ========================================================================

ANIMATION = {
    # Timing (milliseconds)
    "token_move_speed": 400,          # Speed per space when moving
    "token_move_ease": "cubic",       # Easing function for movement
    "dice_roll_duration": 1500,       # Total dice animation time
    "dice_bounce_count": 8,           # Number of dice bounces
    "card_flip_duration": 300,        # Property card flip animation
    "highlight_pulse": 1000,          # Property highlight pulse cycle
    "fade_in_duration": 200,          # Panel fade in time
    "fade_out_duration": 150,         # Panel fade out time
    
    # Visual Effects
    "glow_radius": 4,                 # Glow effect radius
    "shadow_offset": 2,               # Shadow offset distance
    "shadow_blur": 4,                 # Shadow blur amount
    "hover_scale": 1.05,              # Scale on hover
    "click_scale": 0.95,              # Scale on click
}

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def get_property_color(color_group: str) -> str:
    """
    Get the authentic color for a property group
    :param color_group: Property group name
    :return: Hex color code
    """
    return PROPERTY_COLORS.get(color_group, "#FFFFFF")

def get_player_color(player_index: int) -> str:
    """
    Get a unique color for a player token
    :param player_index: Player number (0-based)
    :return: Hex color code
    """
    colors = UI_COLORS["player_colors"]
    return colors[player_index % len(colors)]

def get_player_token_style(player_index: int) -> dict:
    """
    Get complete token style for a player
    :param player_index: Player number (0-based)
    :return: Style dictionary with color, border, etc.
    """
    base_color = get_player_color(player_index)
    return {
        "fill": base_color,
        "outline": darken_color(base_color, 0.6),
        "width": SIZES["token_border"],
        "active_glow": UI_COLORS["token_glow"]
    }

def darken_color(hex_color: str, factor: float = 0.7) -> str:
    """
    Darken a hex color by a factor
    :param hex_color: Hex color code
    :param factor: Darkening factor (0.0 to 1.0)
    :return: Darkened hex color
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * factor)) for c in rgb)
    return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

def lighten_color(hex_color: str, factor: float = 0.3) -> str:
    """
    Lighten a hex color by blending with white
    :param hex_color: Hex color code  
    :param factor: Lightening factor (0.0 to 1.0)
    :return: Lightened hex color
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lightened = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
    return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"

def create_gradient(color1: str, color2: str, steps: int = 10) -> list:
    """
    Create a gradient between two colors
    :param color1: Start color (hex)
    :param color2: End color (hex)
    :param steps: Number of gradient steps
    :return: List of hex colors
    """
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    
    rgb1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
    
    gradient = []
    for step in range(steps):
        factor = step / (steps - 1) if steps > 1 else 0
        r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * factor)
        g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * factor)
        b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * factor)
        gradient.append(f"#{r:02x}{g:02x}{b:02x}")
    
    return gradient

def apply_transparency(hex_color: str, alpha: float = 0.5) -> str:
    """
    Convert hex color to RGBA with transparency
    :param hex_color: Hex color code
    :param alpha: Transparency (0.0 to 1.0)
    :return: RGBA color string for Tkinter
    """
    # Note: Tkinter doesn't support true transparency in colors,
    # this returns the hex color unchanged. For actual transparency,
    # use Canvas items with stipple patterns or images.
    return hex_color