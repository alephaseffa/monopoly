"""
@author: Aleph Aseffa
Authentic Monopoly Board Renderer

High-quality, polished board rendering with authentic Monopoly aesthetics
"""

import tkinter as tk
from tkinter import Canvas
import math
from typing import Dict, List, Tuple, Optional, Any
import colors

class AuthenticMonopolyBoard:
    """Professional Monopoly board with authentic design"""
    
    # Standard Monopoly board layout constants
    PROPERTIES_PER_SIDE = 9
    TOTAL_SPACES = 40
    
    def __init__(self, parent: tk.Widget, board_data: List[Any], 
                 on_property_click: Optional[callable] = None):
        """Initialize authentic Monopoly board"""
        self.parent = parent
        self.board_data = board_data
        self.on_property_click = on_property_click
        
        # Board dimensions
        self.board_size = colors.SIZES["board_size"]
        self.corner_size = colors.SIZES["corner_size"]
        self.property_width = colors.SIZES["property_width"]
        self.property_height = colors.SIZES["property_height"]
        
        # Create main canvas
        self.canvas = self._create_canvas()
        
        # Property tracking
        self.property_rects = {}  # position -> rect_id
        self.property_elements = {}  # position -> {element_type: id}
        
        # Player tracking
        self.player_tokens = {}  # player_name -> token_id
        self.player_positions = {}  # player_name -> position
        
        # Interaction state
        self.highlighted_property = None
        self.selected_property = None
        
        # Draw the board
        self._render_board()
        
        # Setup events
        self._setup_events()
    
    def _create_canvas(self) -> Canvas:
        """Create and configure the main canvas"""
        canvas = Canvas(
            self.parent,
            width=self.board_size,
            height=self.board_size,
            bg=colors.BOARD_COLORS["board_center"],
            highlightthickness=0
        )
        canvas.pack(padx=10, pady=10)
        return canvas
    
    def _render_board(self):
        """Render the complete board"""
        self._draw_background()
        self._draw_all_spaces()
        self._draw_center_logo()
    
    def _draw_background(self):
        """Draw board background and borders"""
        # Outer border
        self.canvas.create_rectangle(
            1, 1, self.board_size - 1, self.board_size - 1,
            fill=colors.BOARD_COLORS["board_edge"],
            width=3,
            outline="#000000"
        )
        
        # Inner play area
        self.canvas.create_rectangle(
            self.corner_size, self.corner_size,
            self.board_size - self.corner_size,
            self.board_size - self.corner_size,
            fill=colors.BOARD_COLORS["board_center"],
            width=2,
            outline=colors.BOARD_COLORS["property_border"]
        )
    
    def _draw_all_spaces(self):
        """Draw all 40 board spaces"""
        for position in range(self.TOTAL_SPACES):
            self._draw_space(position)
    
    def _draw_space(self, position: int):
        """Draw a single board space"""
        x, y, w, h, side = self._get_space_coords(position)
        
        # Get property data
        property_data = self.board_data[position] if position < len(self.board_data) else None
        
        # Draw based on type
        if position in [0, 10, 20, 30]:  # Corners
            self._draw_corner(position, x, y, property_data)
        else:
            self._draw_property(position, x, y, w, h, side, property_data)
    
    def _get_space_coords(self, position: int) -> Tuple[int, int, int, int, str]:
        """Get coordinates and dimensions for a space"""
        board_size = self.board_size
        corner = self.corner_size
        prop_w = self.property_width
        prop_h = self.property_height
        
        if position == 0:  # GO
            return board_size - corner, board_size - corner, corner, corner, "corner"
        elif position < 10:  # Bottom
            x = board_size - corner - position * prop_w
            return x, board_size - prop_h, prop_w, prop_h, "bottom"
        elif position == 10:  # Jail
            return 0, board_size - corner, corner, corner, "corner"
        elif position < 20:  # Left
            y = board_size - corner - (position - 10) * prop_w
            return 0, y, prop_h, prop_w, "left"
        elif position == 20:  # Free Parking
            return 0, 0, corner, corner, "corner"
        elif position < 30:  # Top
            x = corner + (position - 21) * prop_w
            return x, 0, prop_w, prop_h, "top"
        elif position == 30:  # Go to Jail
            return board_size - corner, 0, corner, corner, "corner"
        else:  # Right
            y = corner + (position - 31) * prop_w
            return board_size - prop_h, y, prop_h, prop_w, "right"
    
    def _draw_corner(self, position: int, x: int, y: int, property_data: Any):
        """Draw corner spaces"""
        size = self.corner_size
        
        # Determine corner color
        corner_colors = {
            0: colors.BOARD_COLORS["go_background"],
            10: colors.BOARD_COLORS["jail_background"],
            20: colors.BOARD_COLORS["parking_background"],
            30: colors.BOARD_COLORS["go_to_jail_bg"]
        }
        
        bg_color = corner_colors.get(position, "#FFFFFF")
        
        # Draw corner rectangle
        rect = self.canvas.create_rectangle(
            x, y, x + size, y + size,
            fill=bg_color,
            outline=colors.BOARD_COLORS["property_border"],
            width=2,
            tags=(f"space_{position}", "corner", "clickable")
        )
        
        self.property_rects[position] = rect
        
        # Draw corner-specific content
        center_x = x + size // 2
        center_y = y + size // 2
        
        if position == 0:  # GO
            self.canvas.create_text(
                center_x, center_y - 15,
                text="GO",
                font=("Arial", 24, "bold"),
                fill="white",
                tags=f"text_{position}"
            )
            self.canvas.create_text(
                center_x, center_y + 10,
                text="← COLLECT",
                font=("Arial", 10, "bold"),
                fill="white"
            )
            self.canvas.create_text(
                center_x, center_y + 25,
                text="$200",
                font=("Arial", 12, "bold"),
                fill="white"
            )
            
        elif position == 10:  # Jail
            # Draw jail cell
            self.canvas.create_rectangle(
                x + size // 3, y + 10,
                x + size - 10, y + size // 2,
                fill="",
                outline="black",
                width=3
            )
            # Jail bars
            for i in range(3):
                bar_x = x + size // 3 + 10 + i * 12
                self.canvas.create_line(
                    bar_x, y + 15,
                    bar_x, y + size // 2 - 5,
                    fill="black",
                    width=2
                )
            self.canvas.create_text(
                center_x, y + size - 25,
                text="JUST",
                font=("Arial", 10, "normal"),
                fill="black"
            )
            self.canvas.create_text(
                center_x, y + size - 12,
                text="VISITING",
                font=("Arial", 10, "normal"),
                fill="black"
            )
            
        elif position == 20:  # Free Parking
            self.canvas.create_text(
                center_x, center_y - 10,
                text="FREE",
                font=("Arial", 12, "bold"),
                fill=colors.BOARD_COLORS["parking_text"]
            )
            self.canvas.create_text(
                center_x, center_y + 10,
                text="PARKING",
                font=("Arial", 12, "bold"),
                fill=colors.BOARD_COLORS["parking_text"]
            )
            
        elif position == 30:  # Go to Jail
            self.canvas.create_text(
                center_x, center_y - 15,
                text="GO TO",
                font=("Arial", 11, "bold"),
                fill="white"
            )
            self.canvas.create_text(
                center_x, center_y + 5,
                text="JAIL",
                font=("Arial", 16, "bold"),
                fill="white"
            )
    
    def _draw_property(self, position: int, x: int, y: int, w: int, h: int, 
                      side: str, property_data: Any):
        """Draw property spaces"""
        # Draw property rectangle
        rect = self.canvas.create_rectangle(
            x, y, x + w, y + h,
            fill=colors.BOARD_COLORS["board_surface"],
            outline=colors.BOARD_COLORS["property_border"],
            width=1,
            tags=(f"space_{position}", "property", "clickable")
        )
        
        self.property_rects[position] = rect
        
        if not property_data:
            return
        
        # Get property info
        name = getattr(property_data, 'name', '')
        color_group = getattr(property_data, 'color_group', '')
        cost = getattr(property_data, 'card_cost', 0)
        
        # Draw based on property type
        if self._is_colored_property(color_group):
            self._draw_colored_property(position, x, y, w, h, side, 
                                       name, color_group, cost)
        elif "railroad" in name.lower() or "r.r." in name.lower():
            self._draw_railroad(position, x, y, w, h, side, name)
        elif "electric" in name.lower() or "water" in name.lower():
            self._draw_utility(position, x, y, w, h, side, name)
        elif "tax" in name.lower():
            self._draw_tax(position, x, y, w, h, side, name)
        elif "chance" in name.lower():
            self._draw_chance(position, x, y, w, h, side)
        elif "community" in name.lower():
            self._draw_community_chest(position, x, y, w, h, side)
    
    def _draw_colored_property(self, position: int, x: int, y: int, w: int, h: int,
                              side: str, name: str, color_group: str, cost: Any):
        """Draw colored property with color bar"""
        prop_color = colors.get_property_color(color_group)
        bar_size = colors.SIZES["property_color_bar"]
        
        # Draw color bar based on side
        if side == "bottom":
            self.canvas.create_rectangle(
                x, y, x + w, y + bar_size,
                fill=prop_color,
                outline=colors.BOARD_COLORS["property_border"]
            )
            text_y = y + bar_size + 12
            price_y = y + h - 8
        elif side == "left":
            self.canvas.create_rectangle(
                x + w - bar_size, y, x + w, y + h,
                fill=prop_color,
                outline=colors.BOARD_COLORS["property_border"]
            )
        elif side == "top":
            self.canvas.create_rectangle(
                x, y + h - bar_size, x + w, y + h,
                fill=prop_color,
                outline=colors.BOARD_COLORS["property_border"]
            )
            text_y = y + 10
            price_y = y + h - bar_size - 8
        elif side == "right":
            self.canvas.create_rectangle(
                x, y, x + bar_size, y + h,
                fill=prop_color,
                outline=colors.BOARD_COLORS["property_border"]
            )
        
        # Draw property name (for horizontal properties)
        if side in ["bottom", "top"]:
            # Split name if too long
            name_parts = self._split_name(name.upper())
            for i, part in enumerate(name_parts):
                self.canvas.create_text(
                    x + w // 2, text_y + i * 10,
                    text=part,
                    font=("Arial", 7, "normal"),
                    fill="black"
                )
            
            # Draw price
            if cost and str(cost) != "N/A":
                self.canvas.create_text(
                    x + w // 2, price_y,
                    text=f"${cost}",
                    font=("Arial", 7, "normal"),
                    fill="black"
                )
        else:
            # Vertical text for side properties
            self.canvas.create_text(
                x + w // 2, y + h // 2,
                text=name.upper()[:8],
                font=("Arial", 6, "normal"),
                fill="black",
                angle=90 if side == "left" else 270
            )
    
    def _draw_railroad(self, position: int, x: int, y: int, w: int, h: int,
                      side: str, name: str):
        """Draw railroad space"""
        # Draw train icon
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Simple train representation
        self.canvas.create_rectangle(
            center_x - 12, center_y - 5,
            center_x + 12, center_y + 5,
            fill="black"
        )
        
        # Draw name
        if side in ["bottom", "top"]:
            self.canvas.create_text(
                center_x, y + 10,
                text=name.upper()[:10],
                font=("Arial", 6, "normal"),
                fill="black"
            )
            self.canvas.create_text(
                center_x, y + h - 10,
                text="$200",
                font=("Arial", 7, "normal"),
                fill="black"
            )
    
    def _draw_utility(self, position: int, x: int, y: int, w: int, h: int,
                     side: str, name: str):
        """Draw utility space"""
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw icon based on type
        if "electric" in name.lower():
            # Light bulb
            self.canvas.create_oval(
                center_x - 8, center_y - 10,
                center_x + 8, center_y + 5,
                fill="yellow",
                outline="black",
                width=2
            )
        else:
            # Water drop
            self.canvas.create_oval(
                center_x - 6, center_y - 8,
                center_x + 6, center_y + 8,
                fill="lightblue",
                outline="blue",
                width=2
            )
        
        # Draw name
        if side in ["bottom", "top"]:
            self.canvas.create_text(
                center_x, y + 10,
                text=name.upper()[:10],
                font=("Arial", 6, "normal"),
                fill="black"
            )
    
    def _draw_tax(self, position: int, x: int, y: int, w: int, h: int,
                 side: str, name: str):
        """Draw tax space"""
        center_x = x + w // 2
        center_y = y + h // 2
        
        self.canvas.create_text(
            center_x, center_y - 5,
            text="$",
            font=("Arial", 16, "bold"),
            fill="green"
        )
        
        amount = "200" if "income" in name.lower() else "75"
        self.canvas.create_text(
            center_x, center_y + 15,
            text=f"PAY ${amount}",
            font=("Arial", 7, "bold"),
            fill="black"
        )
    
    def _draw_chance(self, position: int, x: int, y: int, w: int, h: int, side: str):
        """Draw chance space"""
        # Orange background
        self.canvas.create_rectangle(
            x + 3, y + 3, x + w - 3, y + h - 3,
            fill=colors.BOARD_COLORS["chance_background"],
            outline=""
        )
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        self.canvas.create_text(
            center_x, center_y - 5,
            text="?",
            font=("Arial", 20, "bold"),
            fill="black"
        )
        
        self.canvas.create_text(
            center_x, center_y + 15,
            text="CHANCE",
            font=("Arial", 7, "bold"),
            fill="black"
        )
    
    def _draw_community_chest(self, position: int, x: int, y: int, w: int, h: int, 
                             side: str):
        """Draw community chest space"""
        # Blue background
        self.canvas.create_rectangle(
            x + 3, y + 3, x + w - 3, y + h - 3,
            fill=colors.BOARD_COLORS["community_chest_bg"],
            outline=""
        )
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Chest icon
        self.canvas.create_rectangle(
            center_x - 8, center_y - 5,
            center_x + 8, center_y + 5,
            fill="gold",
            outline="darkgoldenrod",
            width=2
        )
        
        self.canvas.create_text(
            center_x, center_y + 15,
            text="CHEST",
            font=("Arial", 7, "bold"),
            fill="black"
        )
    
    def _draw_center_logo(self):
        """Draw Monopoly logo in center"""
        center = self.board_size // 2
        
        self.canvas.create_text(
            center, center - 15,
            text="MONOPOLY",
            font=("Times New Roman", 32, "bold"),
            fill=colors.BOARD_COLORS["go_background"]
        )
        
        self.canvas.create_text(
            center, center + 15,
            text="PROPERTY TRADING GAME",
            font=("Arial", 10, "normal"),
            fill="black"
        )
    
    def _split_name(self, name: str, max_len: int = 10) -> List[str]:
        """Split property name for display"""
        if len(name) <= max_len:
            return [name]
        
        words = name.split()
        if len(words) == 1:
            return [name[:max_len], name[max_len:]]
        
        lines = []
        current = ""
        for word in words:
            if not current:
                current = word
            elif len(current) + len(word) + 1 <= max_len:
                current += " " + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        
        return lines[:2]  # Max 2 lines
    
    def _is_colored_property(self, color_group: str) -> bool:
        """Check if this is a colored property"""
        return color_group in colors.PROPERTY_COLORS and color_group not in ["Railroad", "Utilities"]
    
    def _setup_events(self):
        """Setup mouse events"""
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_hover)
        self.canvas.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event):
        """Handle click events"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        for tag in tags:
            if tag.startswith("space_"):
                position = int(tag.split("_")[1])
                self._select_property(position)
                if self.on_property_click:
                    self.on_property_click(position)
                break
    
    def _on_hover(self, event):
        """Handle hover events"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        for tag in tags:
            if tag.startswith("space_"):
                position = int(tag.split("_")[1])
                self._highlight_property(position)
                break
    
    def _on_leave(self, event):
        """Handle mouse leave"""
        self._clear_highlight()
    
    def _highlight_property(self, position: int):
        """Highlight property on hover"""
        if self.highlighted_property == position:
            return
        
        self._clear_highlight()
        
        if position in self.property_rects:
            rect = self.property_rects[position]
            self.canvas.itemconfig(rect, width=3)
            self.highlighted_property = position
    
    def _clear_highlight(self):
        """Clear property highlight"""
        if self.highlighted_property is not None:
            if self.highlighted_property in self.property_rects:
                rect = self.property_rects[self.highlighted_property]
                self.canvas.itemconfig(rect, width=1 if self.highlighted_property != self.selected_property else 2)
            self.highlighted_property = None
    
    def _select_property(self, position: int):
        """Select a property"""
        # Clear previous selection
        if self.selected_property is not None:
            if self.selected_property in self.property_rects:
                rect = self.property_rects[self.selected_property]
                self.canvas.itemconfig(rect, width=1)
        
        # Set new selection
        if position in self.property_rects:
            rect = self.property_rects[position]
            self.canvas.itemconfig(rect, width=2, 
                                 outline=colors.UI_COLORS["token_glow"])
            self.selected_property = position
    
    def add_player_token(self, player_name: str, player_index: int):
        """Add a player token to the board"""
        x, y, w, h, _ = self._get_space_coords(0)
        
        token_color = colors.get_player_color(player_index)
        token_size = colors.SIZES["token_size"]
        
        # Calculate token position with offset for multiple players
        offset_x, offset_y = self._get_token_offset(player_index)
        token_x = x + w // 2 + offset_x
        token_y = y + h // 2 + offset_y
        
        # Create token
        token = self.canvas.create_oval(
            token_x - token_size // 2,
            token_y - token_size // 2,
            token_x + token_size // 2,
            token_y + token_size // 2,
            fill=token_color,
            outline=darken_color(token_color, 0.6),
            width=2,
            tags=(f"token_{player_name}", "player_token")
        )
        
        self.player_tokens[player_name] = token
        self.player_positions[player_name] = 0
    
    def move_player_token(self, player_name: str, new_position: int, animate: bool = True):
        """Move a player token to a new position"""
        if player_name not in self.player_tokens:
            return
        
        token = self.player_tokens[player_name]
        old_position = self.player_positions.get(player_name, 0)
        
        if animate and old_position != new_position:
            self._animate_movement(player_name, old_position, new_position)
        else:
            self._place_token(player_name, new_position)
    
    def _animate_movement(self, player_name: str, start: int, end: int):
        """Animate token movement"""
        # Calculate path
        path = []
        current = start
        while current != end:
            current = (current + 1) % 40
            path.append(current)
        
        # Start animation
        self._move_along_path(player_name, path, 0)
    
    def _move_along_path(self, player_name: str, path: List[int], index: int):
        """Move token along calculated path"""
        if index >= len(path):
            return
        
        position = path[index]
        self._place_token(player_name, position)
        
        # Continue animation
        self.canvas.after(
            colors.ANIMATION["token_move_speed"],
            lambda: self._move_along_path(player_name, path, index + 1)
        )
    
    def _place_token(self, player_name: str, position: int):
        """Place token at specific position"""
        if player_name not in self.player_tokens:
            return
        
        token = self.player_tokens[player_name]
        x, y, w, h, _ = self._get_space_coords(position)
        
        # Get player index for offset
        player_index = list(self.player_tokens.keys()).index(player_name)
        offset_x, offset_y = self._get_token_offset(player_index)
        
        token_size = colors.SIZES["token_size"]
        token_x = x + w // 2 + offset_x
        token_y = y + h // 2 + offset_y
        
        # Move token
        self.canvas.coords(
            token,
            token_x - token_size // 2,
            token_y - token_size // 2,
            token_x + token_size // 2,
            token_y + token_size // 2
        )
        
        self.player_positions[player_name] = position
    
    def _get_token_offset(self, player_index: int) -> Tuple[int, int]:
        """Calculate offset for multiple tokens on same space"""
        angles = [0, 90, 180, 270, 45, 135, 225, 315]
        angle = angles[player_index % len(angles)]
        radius = 12
        
        offset_x = int(radius * math.cos(math.radians(angle)))
        offset_y = int(radius * math.sin(math.radians(angle)))
        
        return offset_x, offset_y
    
    def highlight_current_player(self, player_name: str):
        """Highlight current player's token"""
        self.canvas.delete("token_highlight")
        
        if player_name in self.player_tokens:
            token = self.player_tokens[player_name]
            bbox = self.canvas.bbox(token)
            
            if bbox:
                # Create glow effect
                self.canvas.create_oval(
                    bbox[0] - 3, bbox[1] - 3,
                    bbox[2] + 3, bbox[3] + 3,
                    fill="",
                    outline=colors.UI_COLORS["token_glow"],
                    width=3,
                    tags="token_highlight"
                )
                
                # Move highlight below token
                self.canvas.tag_lower("token_highlight", token)