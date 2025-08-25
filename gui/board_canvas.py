"""
@author: Aleph Aseffa
Board rendering and animation system for Monopoly GUI

Handles the visual representation of the game board, player tokens,
and property display with full color support.
"""

import tkinter as tk
from tkinter import Canvas
import math
from typing import List, Dict, Tuple, Optional
from .colors import *

class BoardCanvas:
    def __init__(self, parent, board_data, on_property_click=None):
        """
        Initialize the board canvas
        :param parent: Parent tkinter widget
        :param board_data: List of Card objects representing the board
        :param on_property_click: Callback function when property is clicked
        """
        self.parent = parent
        self.board_data = board_data
        self.on_property_click = on_property_click or (lambda pos: None)
        
        # Create canvas
        self.canvas = Canvas(
            parent, 
            width=SIZES["board_size"], 
            height=SIZES["board_size"],
            bg=UI_COLORS["board_background"],
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Property positions and dimensions
        self.property_positions = self._calculate_property_positions()
        self.player_tokens = {}  # player_name -> token_id
        self.player_positions = {}  # player_name -> current_position
        
        # Animation tracking
        self.animations = {}  # player_name -> animation_data
        
        # Property highlighting
        self.highlighted_property = None
        self.selected_property = None
        
        # Draw initial board
        self._draw_board()
        
        # Bind click and hover events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>", self._on_canvas_hover)
        self.canvas.bind("<Leave>", self._on_canvas_leave)
        
    def _calculate_property_positions(self) -> List[Dict]:
        """
        Calculate positions and dimensions for all 40 board spaces
        :return: List of position dictionaries
        """
        positions = []
        board_size = SIZES["board_size"]
        corner_size = SIZES["corner_size"]
        prop_width = SIZES["property_width"]
        prop_height = SIZES["property_height"]
        
        # Bottom row (positions 0-10)
        for i in range(11):
            if i == 0:  # GO corner
                positions.append({
                    "x": board_size - corner_size,
                    "y": board_size - corner_size,
                    "width": corner_size,
                    "height": corner_size,
                    "is_corner": True
                })
            elif i == 10:  # Jail corner
                positions.append({
                    "x": 0,
                    "y": board_size - corner_size,
                    "width": corner_size,
                    "height": corner_size,
                    "is_corner": True
                })
            else:  # Regular properties
                x = board_size - corner_size - i * prop_width
                positions.append({
                    "x": x,
                    "y": board_size - prop_height,
                    "width": prop_width,
                    "height": prop_height,
                    "is_corner": False
                })
        
        # Left side (positions 11-19)
        for i in range(1, 10):
            y = board_size - corner_size - i * prop_width
            positions.append({
                "x": 0,
                "y": y,
                "width": prop_height,
                "height": prop_width,
                "is_corner": False
            })
            
        # Top row (positions 20-30)
        for i in range(11):
            if i == 0:  # Free Parking corner
                positions.append({
                    "x": 0,
                    "y": 0,
                    "width": corner_size,
                    "height": corner_size,
                    "is_corner": True
                })
            elif i == 10:  # Go to Jail corner
                positions.append({
                    "x": board_size - corner_size,
                    "y": 0,
                    "width": corner_size,
                    "height": corner_size,
                    "is_corner": True
                })
            else:  # Regular properties
                x = corner_size + (i - 1) * prop_width
                positions.append({
                    "x": x,
                    "y": 0,
                    "width": prop_width,
                    "height": prop_height,
                    "is_corner": False
                })
        
        # Right side (positions 31-39)
        for i in range(1, 10):
            y = corner_size + (i - 1) * prop_width
            positions.append({
                "x": board_size - prop_height,
                "y": y,
                "width": prop_height,
                "height": prop_width,
                "is_corner": False
            })
            
        return positions
    
    def _draw_board(self):
        """Draw the complete board with all properties"""
        for i, (card, pos) in enumerate(zip(self.board_data, self.property_positions)):
            self._draw_property(i, card, pos)
    
    def _draw_property(self, position: int, card, pos_data: Dict):
        """
        Draw a single property space
        :param position: Board position (0-39)
        :param card: Card object with property data
        :param pos_data: Position and size information
        """
        x, y = pos_data["x"], pos_data["y"]
        width, height = pos_data["width"], pos_data["height"]
        is_corner = pos_data["is_corner"]
        
        # Determine background color
        if is_corner:
            bg_color = self._get_corner_color(card.card_name)
        else:
            bg_color = get_property_color(getattr(card, 'color_group', 'N/A'))
            if bg_color == "#FFFFFF":  # Default for special spaces
                bg_color = self._get_special_space_color(card.card_name)
        
        # Draw property rectangle
        property_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=bg_color,
            outline=UI_COLORS["property_border"],
            width=2,
            tags=f"property_{position}"
        )
        
        # Add property name text
        text_x = x + width // 2
        text_y = y + height // 2
        
        if is_corner:
            font = FONTS["title"]
            text_color = UI_COLORS["text_primary"]
        else:
            font = FONTS["property"]
            text_color = UI_COLORS["property_text"]
            
        # Handle long property names
        display_name = self._format_property_name(card.card_name, width)
        
        text_id = self.canvas.create_text(
            text_x, text_y,
            text=display_name,
            font=font,
            fill=text_color,
            width=width - 10,
            tags=f"property_{position}"
        )
        
        # Add special symbols and pricing
        self._add_property_symbols_and_price(card, x, y, width, height, text_x, text_y, is_corner, position)
    
    def _add_property_symbols_and_price(self, card, x, y, width, height, text_x, text_y, is_corner, position):
        """Add special symbols and price information for properties"""
        
        # Determine property type and add appropriate symbols
        property_type = self._get_property_type(card.card_name, getattr(card, 'color_group', 'N/A'))
        
        # Position for symbols (above text)
        symbol_y = text_y - 20 if not is_corner else text_y - 25
        
        if property_type == 'railroad':
            # Add railroad symbol
            self.canvas.create_text(
                text_x, symbol_y,
                text="🚂",
                font=("Arial", 16, "normal"),
                fill=UI_COLORS["text_primary"],
                tags=f"property_{position}"
            )
        elif property_type == 'utility':
            # Add utility symbol based on specific utility
            symbol = "⚡" if "Electric" in card.card_name else "💧"
            self.canvas.create_text(
                text_x, symbol_y,
                text=symbol,
                font=("Arial", 16, "normal"),
                fill=UI_COLORS["text_primary"],
                tags=f"property_{position}"
            )
        elif property_type == 'tax':
            # Add tax symbol
            self.canvas.create_text(
                text_x, symbol_y,
                text="💰",
                font=("Arial", 14, "normal"),
                fill=UI_COLORS["text_error"],
                tags=f"property_{position}"
            )
            
            # For tax spaces, show the tax amount instead of purchase price
            tax_amount = "$200" if "Income" in card.card_name else "$75"
            price_y = text_y + 15 if is_corner else text_y + 12
            self.canvas.create_text(
                text_x, price_y,
                text=tax_amount,
                font=("Arial", 8, "bold"),
                fill=UI_COLORS["text_error"],
                tags=f"property_{position}"
            )
            return  # Early return for tax spaces
        
        elif property_type == 'chance':
            # Add chance symbol
            self.canvas.create_text(
                text_x, symbol_y,
                text="?",
                font=("Arial", 20, "bold"),
                fill="white",
                tags=f"property_{position}"
            )
        elif property_type == 'community_chest':
            # Add community chest symbol
            self.canvas.create_text(
                text_x, symbol_y,
                text="📦",
                font=("Arial", 14, "normal"),
                fill=UI_COLORS["text_primary"],
                tags=f"property_{position}"
            )
        
        # Add price for purchasable properties (not tax spaces)
        if hasattr(card, 'card_cost') and card.card_cost != "N/A" and property_type not in ['tax', 'chance', 'community_chest']:
            price_y = text_y + 15 if is_corner else text_y + 12
            self.canvas.create_text(
                text_x, price_y,
                text=f"${card.card_cost}",
                font=("Arial", 8, "bold"),
                fill=UI_COLORS["text_highlight"],
                tags=f"property_{position}"
            )
    
    def _get_property_type(self, name: str, color_group: str) -> str:
        """Determine the type of property based on name and color group"""
        name_upper = name.upper()
        
        if "RAILROAD" in name_upper or color_group == "Railroad":
            return 'railroad'
        elif "ELECTRIC" in name_upper or "WATER" in name_upper or color_group == "Utilities":
            return 'utility'
        elif "TAX" in name_upper:
            return 'tax'
        elif "CHANCE" in name_upper:
            return 'chance'
        elif "COMMUNITY CHEST" in name_upper:
            return 'community_chest'
        elif name_upper in ["GO", "JAIL", "FREE PARKING", "GO TO JAIL"]:
            return 'corner'
        else:
            return 'property'
    
    def _get_corner_color(self, name: str) -> str:
        """Get color for corner spaces"""
        if "GO" in name.upper():
            return UI_COLORS["go_color"]
        elif "JAIL" in name.upper():
            return UI_COLORS["jail_color"]
        elif "PARKING" in name.upper():
            return UI_COLORS["parking_color"]
        elif "GO TO JAIL" in name.upper():
            return UI_COLORS["jail_color"]
        else:
            return UI_COLORS["background"]
    
    def _get_special_space_color(self, name: str) -> str:
        """Get color for special non-corner spaces"""
        if "TAX" in name.upper():
            return UI_COLORS["tax_color"]
        elif "CHANCE" in name.upper():
            return UI_COLORS["chance_color"]
        elif "COMMUNITY CHEST" in name.upper():
            return UI_COLORS["community_chest_color"]
        else:
            return UI_COLORS["background"]
    
    def _format_property_name(self, name: str, max_width: int) -> str:
        """Format property name to fit in space with intelligent word wrapping"""
        # Short names don't need formatting
        if len(name) <= 10:
            return name
        
        # Handle specific known long property names with good breaks
        name_overrides = {
            "Mediterranean Avenue": "Mediterranean\nAvenue",
            "Baltic Avenue": "Baltic\nAvenue", 
            "Oriental Avenue": "Oriental\nAvenue",
            "Vermont Avenue": "Vermont\nAvenue",
            "Connecticut Avenue": "Connecticut\nAvenue",
            "St. Charles Place": "St. Charles\nPlace",
            "Electric Company": "Electric\nCompany",
            "States Avenue": "States\nAvenue",
            "Virginia Avenue": "Virginia\nAvenue",
            "St. James Place": "St. James\nPlace",
            "Tennessee Avenue": "Tennessee\nAvenue",
            "New York Avenue": "New York\nAvenue",
            "Kentucky Avenue": "Kentucky\nAvenue",
            "Indiana Avenue": "Indiana\nAvenue",
            "Illinois Avenue": "Illinois\nAvenue",
            "Atlantic Avenue": "Atlantic\nAvenue",
            "Ventnor Avenue": "Ventnor\nAvenue",
            "Water Works": "Water\nWorks",
            "Marvin Gardens": "Marvin\nGardens",
            "Pacific Avenue": "Pacific\nAvenue",
            "North Carolina Avenue": "N. Carolina\nAvenue",
            "Pennsylvania Avenue": "Pennsylvania\nAvenue",
            "Park Place": "Park\nPlace",
            "Pennsylvania Railroad": "Pennsylvania\nRailroad",
            "Reading Railroad": "Reading\nRailroad",
            "B. & O. Railroad": "B. & O.\nRailroad",
            "Short Line": "Short\nLine"
        }
        
        if name in name_overrides:
            return name_overrides[name]
        
        # General algorithm for other names
        words = name.split()
        if len(words) == 1:
            # Single word - try to break at reasonable point or truncate
            if len(name) > 12:
                return name[:9] + "..."
            return name
        
        # Multiple words - find best break point
        if len(words) == 2:
            return f"{words[0]}\n{words[1]}"
        
        # For 3+ words, try to balance line lengths
        total_length = len(name)
        if total_length <= 16:
            # Try to fit in 2 lines with good balance
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            
            # Adjust if lines are very unbalanced
            if abs(len(line1) - len(line2)) > 4 and len(words) > 2:
                if len(line1) > len(line2):
                    # Move one word from line1 to line2
                    if mid > 1:
                        line1 = " ".join(words[:mid-1])
                        line2 = " ".join(words[mid-1:])
                else:
                    # Move one word from line2 to line1
                    if mid < len(words) - 1:
                        line1 = " ".join(words[:mid+1])
                        line2 = " ".join(words[mid+1:])
            
            return f"{line1}\n{line2}"
        
        # Very long names - abbreviate
        if "Avenue" in name:
            name = name.replace("Avenue", "Ave")
        if "Street" in name:
            name = name.replace("Street", "St")
        if "Place" in name:
            name = name.replace("Place", "Pl")
        
        return self._format_property_name(name, max_width)  # Retry with abbreviations
    
    def add_player(self, player_name: str, player_index: int, position: int = 0):
        """
        Add a player token to the board with distinct shapes
        :param player_name: Name of the player
        :param player_index: Index for color assignment and shape
        :param position: Starting position (default 0 for GO)
        """
        color = get_player_color(player_index)
        token_pos = self._get_token_position(position, len(self.player_tokens))
        
        # Create token shape based on player index
        token_id = self._create_player_token(token_pos[0], token_pos[1], player_index, color, player_name)
        
        self.player_tokens[player_name] = token_id
        self.player_positions[player_name] = position
    
    def _create_player_token(self, x: int, y: int, player_index: int, color: str, player_name: str) -> int:
        """Create a distinct token shape for each player"""
        size = SIZES["token_size"]
        outline_color = darken_color(color)
        
        # Different shapes for each player
        if player_index == 0:  # Circle (traditional)
            token_id = self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline=outline_color, width=3,
                tags=f"token_{player_name}"
            )
        elif player_index == 1:  # Square
            token_id = self.canvas.create_rectangle(
                x - size, y - size, x + size, y + size,
                fill=color, outline=outline_color, width=3,
                tags=f"token_{player_name}"
            )
        elif player_index == 2:  # Diamond
            points = [x, y - size, x + size, y, x, y + size, x - size, y]
            token_id = self.canvas.create_polygon(
                points,
                fill=color, outline=outline_color, width=3,
                tags=f"token_{player_name}"
            )
        elif player_index == 3:  # Triangle
            points = [x, y - size, x + size, y + size, x - size, y + size]
            token_id = self.canvas.create_polygon(
                points,
                fill=color, outline=outline_color, width=3,
                tags=f"token_{player_name}"
            )
        elif player_index == 4:  # Hexagon
            import math
            points = []
            for i in range(6):
                angle = i * math.pi / 3
                px = x + size * math.cos(angle)
                py = y + size * math.sin(angle)
                points.extend([px, py])
            token_id = self.canvas.create_polygon(
                points,
                fill=color, outline=outline_color, width=3,
                tags=f"token_{player_name}"
            )
        else:  # Star for additional players
            import math
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                radius = size if i % 2 == 0 else size * 0.5
                px = x + radius * math.cos(angle - math.pi/2)
                py = y + radius * math.sin(angle - math.pi/2)
                points.extend([px, py])
            token_id = self.canvas.create_polygon(
                points,
                fill=color, outline=outline_color, width=2,
                tags=f"token_{player_name}"
            )
        
        # Add player initial or symbol
        text_color = "white" if self._is_dark_color(color) else "black"
        initial = player_name[0].upper() if player_name != "AI" else "🤖"
        self.canvas.create_text(
            x, y,
            text=initial,
            font=("Arial", 9, "bold"),
            fill=text_color,
            tags=f"token_{player_name}"
        )
        
        return token_id
    
    def _is_dark_color(self, color: str) -> bool:
        """Check if a color is dark (for text contrast)"""
        # Remove # if present
        color = color.lstrip('#')
        
        # Convert to RGB
        r = int(color[0:2], 16)
        g = int(color[2:4], 16) 
        b = int(color[4:6], 16)
        
        # Calculate perceived brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128
    
    def _get_token_position(self, board_position: int, token_offset: int = 0) -> Tuple[int, int]:
        """
        Get pixel coordinates for a token at a board position
        :param board_position: Board position (0-39)
        :param token_offset: Offset for multiple tokens on same space
        :return: (x, y) pixel coordinates
        """
        pos_data = self.property_positions[board_position]
        
        # Center of the property space
        center_x = pos_data["x"] + pos_data["width"] // 2
        center_y = pos_data["y"] + pos_data["height"] // 2
        
        # Offset for multiple players on same space
        offset_x = (token_offset % 2) * 15 - 7
        offset_y = (token_offset // 2) * 15 - 7
        
        return center_x + offset_x, center_y + offset_y
    
    def move_player_token(self, player_name: str, new_position: int, animate: bool = True):
        """
        Move a player token to a new position
        :param player_name: Name of the player
        :param new_position: New board position
        :param animate: Whether to animate the movement
        """
        if player_name not in self.player_tokens:
            return
            
        old_position = self.player_positions.get(player_name, 0)
        self.player_positions[player_name] = new_position
        
        if animate:
            self._animate_token_movement(player_name, old_position, new_position)
        else:
            # Move instantly
            token_pos = self._get_token_position(new_position, 0)  # TODO: Calculate proper offset
            self.canvas.coords(
                self.player_tokens[player_name],
                token_pos[0] - SIZES["token_size"],
                token_pos[1] - SIZES["token_size"],
                token_pos[0] + SIZES["token_size"],
                token_pos[1] + SIZES["token_size"]
            )
    
    def _animate_token_movement(self, player_name: str, start_pos: int, end_pos: int):
        """
        Animate token movement between positions
        :param player_name: Name of the player
        :param start_pos: Starting board position
        :param end_pos: Ending board position
        """
        # Calculate path (handle wrapping around the board)
        if end_pos < start_pos:
            end_pos += 40  # Handle going around the board
            
        positions_to_visit = list(range(start_pos, end_pos + 1))
        
        # Start animation
        self.animations[player_name] = {
            "positions": [pos % 40 for pos in positions_to_visit],
            "current_step": 0,
            "total_steps": len(positions_to_visit) - 1
        }
        
        self._animation_step(player_name)
    
    def _animation_step(self, player_name: str):
        """Execute one step of token animation"""
        if player_name not in self.animations:
            return
            
        anim_data = self.animations[player_name]
        positions = anim_data["positions"]
        step = anim_data["current_step"]
        
        if step < len(positions):
            # Move to next position
            current_pos = positions[step]
            token_pos = self._get_token_position(current_pos, 0)  # TODO: Handle multiple players
            
            # Update token position
            token_tags = f"token_{player_name}"
            token_items = self.canvas.find_withtag(token_tags)
            
            if token_items:
                # Move oval
                self.canvas.coords(
                    token_items[0],  # Oval
                    token_pos[0] - SIZES["token_size"],
                    token_pos[1] - SIZES["token_size"],
                    token_pos[0] + SIZES["token_size"],
                    token_pos[1] + SIZES["token_size"]
                )
                
                # Move text
                if len(token_items) > 1:
                    self.canvas.coords(token_items[1], token_pos[0], token_pos[1])
            
            # Schedule next step
            anim_data["current_step"] += 1
            self.canvas.after(ANIMATION["token_move_speed"], lambda: self._animation_step(player_name))
        else:
            # Animation complete
            del self.animations[player_name]
    
    def highlight_property(self, position: int, highlight: bool = True):
        """
        Highlight or unhighlight a property
        :param position: Board position to highlight
        :param highlight: True to highlight, False to remove highlight
        """
        tag = f"property_{position}"
        items = self.canvas.find_withtag(tag)
        
        if items and highlight:
            # Add highlight border
            pos_data = self.property_positions[position]
            self.canvas.create_rectangle(
                pos_data["x"] - 2, pos_data["y"] - 2,
                pos_data["x"] + pos_data["width"] + 2,
                pos_data["y"] + pos_data["height"] + 2,
                fill="",
                outline=UI_COLORS["text_highlight"],
                width=4,
                tags=f"highlight_{position}"
            )
        else:
            # Remove highlight
            self.canvas.delete(f"highlight_{position}")
    
    def update_property_ownership(self, position: int, owner_name: str):
        """
        Update visual indication of property ownership
        :param position: Board position
        :param owner_name: Name of the owner (or "Bank" for unowned)
        """
        pos_data = self.property_positions[position]
        
        # Remove existing ownership indicator
        self.canvas.delete(f"owner_{position}")
        
        if owner_name != "Bank":
            # Add ownership indicator (small colored dot)
            x = pos_data["x"] + pos_data["width"] - 15
            y = pos_data["y"] + 5
            
            # Use player color or default
            owner_color = UI_COLORS["owned_indicator"]
            
            self.canvas.create_oval(
                x, y, x + 10, y + 10,
                fill=owner_color,
                outline=darken_color(owner_color),
                tags=f"owner_{position}"
            )
    
    def _on_canvas_click(self, event):
        """Handle canvas click events with visual feedback"""
        x, y = event.x, event.y
        
        # Find which property was clicked
        clicked_position = self._get_property_at_position(x, y)
        
        if clicked_position is not None:
            # Update selection
            self._set_selected_property(clicked_position)
            
            # Call the callback
            self.on_property_click(clicked_position)
    
    def _on_canvas_hover(self, event):
        """Handle canvas hover for property highlighting"""
        x, y = event.x, event.y
        
        # Find which property is being hovered over
        hovered_position = self._get_property_at_position(x, y)
        
        if hovered_position != self.highlighted_property:
            self._set_highlighted_property(hovered_position)
    
    def _on_canvas_leave(self, event):
        """Handle canvas leave to remove hover effects"""
        self._set_highlighted_property(None)
    
    def _get_property_at_position(self, x: int, y: int) -> Optional[int]:
        """Get property position at pixel coordinates"""
        for position, pos_data in enumerate(self.property_positions):
            if (pos_data["x"] <= x <= pos_data["x"] + pos_data["width"] and
                pos_data["y"] <= y <= pos_data["y"] + pos_data["height"]):
                return position
        return None
    
    def _set_highlighted_property(self, position: Optional[int]):
        """Set the highlighted property with visual feedback"""
        # Clear previous highlight
        if self.highlighted_property is not None:
            self._remove_property_highlight(self.highlighted_property)
        
        # Set new highlight
        self.highlighted_property = position
        if position is not None:
            self._add_property_highlight(position, "hover")
    
    def _set_selected_property(self, position: Optional[int]):
        """Set the selected property with visual feedback"""
        # Clear previous selection
        if self.selected_property is not None:
            self._remove_property_selection(self.selected_property)
        
        # Set new selection
        self.selected_property = position
        if position is not None:
            self._add_property_selection(position)
    
    def _add_property_highlight(self, position: int, highlight_type: str = "hover"):
        """Add visual highlight to property"""
        pos_data = self.property_positions[position]
        
        # Choose highlight color based on type
        if highlight_type == "hover":
            color = UI_COLORS["text_highlight"]
            width = 3
            tag_suffix = "hover"
        else:
            color = UI_COLORS["text_success"]
            width = 4
            tag_suffix = "select"
        
        # Draw highlight border
        self.canvas.create_rectangle(
            pos_data["x"] - 2, pos_data["y"] - 2,
            pos_data["x"] + pos_data["width"] + 2,
            pos_data["y"] + pos_data["height"] + 2,
            outline=color,
            width=width,
            fill="",
            tags=f"highlight_{tag_suffix}_{position}"
        )
    
    def _remove_property_highlight(self, position: int):
        """Remove visual highlight from property"""
        self.canvas.delete(f"highlight_hover_{position}")
    
    def _add_property_selection(self, position: int):
        """Add visual selection to property"""
        self._add_property_highlight(position, "select")
    
    def _remove_property_selection(self, position: int):
        """Remove visual selection from property"""
        self.canvas.delete(f"highlight_select_{position}")
    
    def clear_property_selection(self):
        """Clear the current property selection"""
        self._set_selected_property(None)
    
    def get_canvas(self):
        """Return the tkinter Canvas widget"""
        return self.canvas