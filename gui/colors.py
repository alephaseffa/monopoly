"""
@author: Aleph Aseffa
Color scheme and visual constants for Monopoly GUI

Contains official Monopoly colors and UI theme definitions
"""

# Official Monopoly Property Group Colors
PROPERTY_COLORS = {
    "Brown": "#8B4513",
    "Light Blue": "#87CEEB", 
    "Pink": "#FF69B4",
    "Orange": "#FFA500",
    "Red": "#DC143C",
    "Yellow": "#FFD700",
    "Green": "#228B22",
    "Blue": "#000080",
    "Railroad": "#000000",
    "Utilities": "#FFFFFF"
}

# UI Theme Colors
UI_COLORS = {
    # Main window and backgrounds
    "background": "#F5F5DC",           # Beige background
    "board_background": "#2F4F2F",     # Dark green board center
    "panel_background": "#F0F8FF",     # Alice blue for panels
    
    # Buttons and controls
    "button_primary": "#32CD32",       # Lime green for main actions
    "button_secondary": "#4169E1",     # Royal blue for secondary actions
    "button_disabled": "#C0C0C0",      # Silver for disabled buttons
    "button_hover": "#98FB98",         # Pale green for hover states
    
    # Text colors
    "text_primary": "#000000",         # Black for main text
    "text_secondary": "#696969",       # Dim gray for secondary text
    "text_highlight": "#FF4500",       # Orange red for highlights
    "text_success": "#228B22",         # Forest green for success messages
    "text_error": "#DC143C",           # Crimson for error messages
    
    # Player colors - distinct, high-contrast colors for better visibility
    "player_colors": ["#FF6B6B", "#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#795548"],
    
    # Special spaces
    "go_color": "#FFD700",             # Gold for GO space
    "jail_color": "#FF4500",           # Orange red for jail
    "parking_color": "#32CD32",        # Lime green for free parking
    "tax_color": "#DC143C",            # Crimson for tax spaces
    "chance_color": "#FF69B4",         # Hot pink for chance
    "community_chest_color": "#87CEEB", # Sky blue for community chest
    
    # Board elements
    "property_border": "#000000",      # Black borders around properties
    "property_text": "#000000",        # Black text on properties
    "owned_indicator": "#FFD700",      # Gold indicator for owned properties
    "mortgaged_overlay": "#FF0000",    # Red overlay for mortgaged properties
}

# Size constants
SIZES = {
    "window_width": 1200,
    "window_height": 900,
    "board_size": 700,
    "property_width": 80,
    "property_height": 120,
    "corner_size": 120,
    "token_size": 12,
    "dice_size": 40,
    "panel_width": 250,
}

# Fonts
FONTS = {
    "title": ("Arial", 16, "bold"),
    "property": ("Arial", 8, "normal"),
    "player": ("Arial", 12, "normal"),
    "button": ("Arial", 10, "bold"),
    "status": ("Arial", 11, "normal"),
    "dice": ("Arial", 14, "bold"),
}

# Animation settings  
ANIMATION = {
    "token_move_speed": 300,  # milliseconds per space
    "dice_roll_duration": 1000,  # milliseconds
    "fade_duration": 200,  # milliseconds
    "property_highlight_duration": 500,  # milliseconds
}

def get_property_color(color_group):
    """
    Get the color for a property group
    :param color_group: str, the color group name
    :return: str, hex color code
    """
    return PROPERTY_COLORS.get(color_group, "#FFFFFF")

def get_player_color(player_index):
    """
    Get a unique color for a player
    :param player_index: int, player number (0-based)
    :return: str, hex color code
    """
    colors = UI_COLORS["player_colors"]
    return colors[player_index % len(colors)]

def darken_color(hex_color, factor=0.7):
    """
    Darken a hex color by a factor
    :param hex_color: str, hex color code
    :param factor: float, darkening factor (0.0 to 1.0)
    :return: str, darkened hex color
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(int(c * factor) for c in rgb)
    return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

def lighten_color(hex_color, factor=0.5):
    """
    Lighten a hex color by a factor
    :param hex_color: str, hex color code  
    :param factor: float, lightening factor (0.0 to 1.0)
    :return: str, lightened hex color
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lightened = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
    return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"