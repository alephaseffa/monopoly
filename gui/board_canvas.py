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
        
        # Draw initial board
        self._draw_board()
        
        # Bind click events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
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
        
        # Add price for purchasable properties
        if hasattr(card, 'card_cost') and card.card_cost != "N/A":
            price_y = text_y + 15 if is_corner else text_y + 12
            self.canvas.create_text(
                text_x, price_y,
                text=f"${card.card_cost}",
                font=("Arial", 8, "bold"),
                fill=UI_COLORS["text_highlight"],
                tags=f"property_{position}"
            )
    
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
        """Format property name to fit in space"""
        if len(name) <= 12:
            return name
        
        # Split long names into multiple lines
        words = name.split()
        if len(words) > 1:
            mid = len(words) // 2
            return "\n".join([" ".join(words[:mid]), " ".join(words[mid:])])
        else:
            # Single long word - truncate with ellipsis
            return name[:10] + "..." if len(name) > 10 else name
    
    def add_player(self, player_name: str, player_index: int, position: int = 0):
        """
        Add a player token to the board
        :param player_name: Name of the player
        :param player_index: Index for color assignment
        :param position: Starting position (default 0 for GO)
        """
        color = get_player_color(player_index)
        token_pos = self._get_token_position(position, len(self.player_tokens))
        
        token_id = self.canvas.create_oval(
            token_pos[0] - SIZES["token_size"],
            token_pos[1] - SIZES["token_size"],
            token_pos[0] + SIZES["token_size"],
            token_pos[1] + SIZES["token_size"],
            fill=color,
            outline=darken_color(color),
            width=2,
            tags=f"token_{player_name}"
        )
        
        # Add player initial
        initial = player_name[0].upper()
        self.canvas.create_text(
            token_pos[0], token_pos[1],
            text=initial,
            font=("Arial", 8, "bold"),
            fill="white",
            tags=f"token_{player_name}"
        )
        
        self.player_tokens[player_name] = token_id
        self.player_positions[player_name] = position
    
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
        """Handle canvas click events"""
        x, y = event.x, event.y
        
        # Find which property was clicked
        for position, pos_data in enumerate(self.property_positions):
            if (pos_data["x"] <= x <= pos_data["x"] + pos_data["width"] and
                pos_data["y"] <= y <= pos_data["y"] + pos_data["height"]):
                self.on_property_click(position)
                break
    
    def get_canvas(self):
        """Return the tkinter Canvas widget"""
        return self.canvas