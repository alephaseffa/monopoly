"""
@author: Aleph Aseffa
UI Panels for Monopoly GUI

Contains all the user interface panels including player information,
game controls, property details, and event log.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Any, Optional
import random
from .colors import *

class PlayerInfoPanel:
    """Panel showing information about all players"""
    
    def __init__(self, parent, players_data: List[Dict], on_player_selected: Optional[Callable] = None):
        """
        Initialize player info panel
        :param parent: Parent widget
        :param players_data: List of player information dictionaries
        :param on_player_selected: Callback when player is selected
        """
        self.parent = parent
        self.on_player_selected = on_player_selected
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=UI_COLORS["panel_background"], relief="raised", bd=2)
        
        # Title
        title = tk.Label(
            self.frame,
            text="PLAYERS",
            font=FONTS["title"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        )
        title.pack(pady=5)
        
        # Player widgets container
        self.player_widgets = {}
        self.players_frame = tk.Frame(self.frame, bg=UI_COLORS["panel_background"])
        self.players_frame.pack(fill="x", padx=10, pady=5)
        
        # Initialize player displays
        for i, player_data in enumerate(players_data):
            self._create_player_widget(i, player_data)
    
    def _create_player_widget(self, player_index: int, player_data: Dict):
        """Create widget for individual player"""
        player_name = player_data["name"]
        player_color = get_player_color(player_index)
        
        # Player frame
        player_frame = tk.Frame(
            self.players_frame,
            bg=lighten_color(player_color, 0.8),
            relief="solid",
            bd=1
        )
        player_frame.pack(fill="x", pady=2)
        
        # Player name with color indicator
        name_frame = tk.Frame(player_frame, bg=lighten_color(player_color, 0.8))
        name_frame.pack(fill="x", padx=5, pady=3)
        
        # Color dot
        color_canvas = tk.Canvas(name_frame, width=12, height=12, highlightthickness=0, bg=lighten_color(player_color, 0.8))
        color_canvas.pack(side="left", padx=(0, 5))
        color_canvas.create_oval(2, 2, 10, 10, fill=player_color, outline=darken_color(player_color))
        
        # Player name
        name_label = tk.Label(
            name_frame,
            text=player_name,
            font=FONTS["player"],
            bg=lighten_color(player_color, 0.8),
            fg=UI_COLORS["text_primary"]
        )
        name_label.pack(side="left")
        
        # Current player indicator
        current_indicator = tk.Label(
            name_frame,
            text="►",
            font=("Arial", 12, "bold"),
            bg=lighten_color(player_color, 0.8),
            fg=UI_COLORS["text_highlight"]
        )
        current_indicator.pack(side="right")
        current_indicator.pack_forget()  # Initially hidden
        
        # Player stats
        stats_frame = tk.Frame(player_frame, bg=lighten_color(player_color, 0.8))
        stats_frame.pack(fill="x", padx=5, pady=2)
        
        # Balance
        balance_label = tk.Label(
            stats_frame,
            text=f"Balance: ${player_data['balance']}",
            font=FONTS["status"],
            bg=lighten_color(player_color, 0.8),
            fg=UI_COLORS["text_primary"]
        )
        balance_label.pack(anchor="w")
        
        # Properties
        properties_label = tk.Label(
            stats_frame,
            text=f"Properties: {player_data['properties']}",
            font=FONTS["status"],
            bg=lighten_color(player_color, 0.8),
            fg=UI_COLORS["text_secondary"]
        )
        properties_label.pack(anchor="w")
        
        # Status indicators
        status_frame = tk.Frame(stats_frame, bg=lighten_color(player_color, 0.8))
        status_frame.pack(fill="x")
        
        jail_status = tk.Label(
            status_frame,
            text="",
            font=("Arial", 9, "normal"),
            bg=lighten_color(player_color, 0.8),
            fg=UI_COLORS["text_error"]
        )
        jail_status.pack(side="left")
        
        # Store widget references
        self.player_widgets[player_name] = {
            "frame": player_frame,
            "name_label": name_label,
            "current_indicator": current_indicator,
            "balance_label": balance_label,
            "properties_label": properties_label,
            "jail_status": jail_status,
            "color": player_color
        }
    
    def update_player_info(self, player_name: str, player_data: Dict):
        """Update player information display"""
        if player_name not in self.player_widgets:
            return
            
        widgets = self.player_widgets[player_name]
        
        # Update balance
        widgets["balance_label"].config(text=f"Balance: ${player_data['balance']}")
        
        # Update properties
        widgets["properties_label"].config(text=f"Properties: {player_data['properties']}")
        
        # Update jail status
        jail_text = ""
        if player_data.get("in_jail", False):
            jail_text = "IN JAIL"
        elif player_data.get("bankrupt", False):
            jail_text = "BANKRUPT"
            
        widgets["jail_status"].config(text=jail_text)
        
        # Update frame color if bankrupt
        if player_data.get("bankrupt", False):
            widgets["frame"].config(bg=UI_COLORS["button_disabled"])
    
    def set_current_player(self, player_name: str):
        """Highlight the current player with enhanced visual feedback"""
        # Reset all players to normal appearance
        for name, widgets in self.player_widgets.items():
            widgets["current_indicator"].pack_forget()
            # Reset frame appearance
            normal_bg = lighten_color(widgets["color"], 0.8)
            widgets["frame"].config(bg=normal_bg, relief="solid", bd=1)
            
            # Reset all child widgets background
            for widget_key in ["name_label", "balance_label", "properties_label", "jail_status"]:
                if widget_key in widgets:
                    widgets[widget_key].config(bg=normal_bg)
        
        # Highlight current player
        if player_name in self.player_widgets:
            widgets = self.player_widgets[player_name]
            
            # Show turn indicator
            widgets["current_indicator"].pack(side="right")
            
            # Enhanced highlighting - brighter background and stronger border
            highlighted_bg = lighten_color(widgets["color"], 0.6)
            widgets["frame"].config(bg=highlighted_bg, relief="raised", bd=3)
            
            # Update all child widgets to use highlighted background
            for widget_key in ["name_label", "balance_label", "properties_label", "jail_status"]:
                if widget_key in widgets:
                    widgets[widget_key].config(bg=highlighted_bg)
            
            # Add pulsing effect to current indicator
            self._pulse_current_indicator(widgets["current_indicator"])
    
    def _pulse_current_indicator(self, indicator_widget):
        """Add a subtle pulsing animation to the current player indicator"""
        def pulse():
            try:
                # Toggle between normal and highlighted
                current_color = indicator_widget.cget("fg")
                new_color = UI_COLORS["text_highlight"] if current_color != UI_COLORS["text_highlight"] else UI_COLORS["text_success"]
                indicator_widget.config(fg=new_color)
                # Schedule next pulse
                indicator_widget.after(800, pulse)
            except tk.TclError:
                # Widget destroyed, stop pulsing
                pass
        pulse()
    
    def get_frame(self):
        """Return the main frame widget"""
        return self.frame

class ActionControlPanel:
    """Panel with game action controls"""
    
    def __init__(self, parent, on_roll_dice: Callable, on_buy_property: Callable, 
                 on_skip_purchase: Callable, on_end_turn: Callable):
        """
        Initialize action control panel
        :param parent: Parent widget
        :param on_roll_dice: Callback for rolling dice
        :param on_buy_property: Callback for buying property
        :param on_skip_purchase: Callback for skipping purchase
        :param on_end_turn: Callback for ending turn
        """
        self.on_roll_dice = on_roll_dice
        self.on_buy_property = on_buy_property
        self.on_skip_purchase = on_skip_purchase
        self.on_end_turn = on_end_turn
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=UI_COLORS["panel_background"], relief="raised", bd=2)
        
        # Title
        title = tk.Label(
            self.frame,
            text="GAME CONTROLS",
            font=FONTS["title"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        )
        title.pack(pady=5)
        
        # Dice display area
        self.dice_frame = tk.Frame(self.frame, bg=UI_COLORS["panel_background"])
        self.dice_frame.pack(pady=10)
        
        self.dice_canvas = tk.Canvas(
            self.dice_frame,
            width=100, height=50,
            bg=UI_COLORS["background"],
            highlightthickness=1,
            highlightbackground=UI_COLORS["property_border"]
        )
        self.dice_canvas.pack()
        
        # Dice result label
        self.dice_result_label = tk.Label(
            self.dice_frame,
            text="Roll to start!",
            font=FONTS["dice"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        )
        self.dice_result_label.pack(pady=5)
        
        # Action buttons
        self.buttons_frame = tk.Frame(self.frame, bg=UI_COLORS["panel_background"])
        self.buttons_frame.pack(pady=10, padx=10, fill="x")
        
        # Roll Dice button with enhanced feedback
        self.roll_button = tk.Button(
            self.buttons_frame,
            text="🎲 ROLL DICE",
            font=FONTS["button"],
            bg=UI_COLORS["button_primary"],
            fg="white",
            relief="raised",
            bd=3,
            command=self._handle_roll_dice,
            cursor="hand2",
            activebackground=lighten_color(UI_COLORS["button_primary"], 0.8),
            activeforeground="white"
        )
        self.roll_button.pack(fill="x", pady=2)
        self._add_button_hover_effects(self.roll_button, UI_COLORS["button_primary"])
        
        # Buy Property button with enhanced feedback
        self.buy_button = tk.Button(
            self.buttons_frame,
            text="💰 BUY PROPERTY",
            font=FONTS["button"],
            bg=UI_COLORS["button_secondary"],
            fg="white",
            relief="raised",
            bd=3,
            command=self._handle_buy_property,
            cursor="hand2",
            state="disabled",
            activebackground=lighten_color(UI_COLORS["button_secondary"], 0.8),
            activeforeground="white"
        )
        self.buy_button.pack(fill="x", pady=2)
        self._add_button_hover_effects(self.buy_button, UI_COLORS["button_secondary"])
        
        # Skip Purchase button with enhanced feedback
        self.skip_button = tk.Button(
            self.buttons_frame,
            text="❌ SKIP PURCHASE",
            font=FONTS["button"],
            bg=UI_COLORS["button_disabled"],
            fg=UI_COLORS["text_secondary"],
            relief="raised",
            bd=3,
            command=self._handle_skip_purchase,
            cursor="hand2",
            state="disabled",
            activebackground=lighten_color(UI_COLORS["button_primary"], 0.8),
            activeforeground="white"
        )
        self.skip_button.pack(fill="x", pady=2)
        self._add_button_hover_effects(self.skip_button, UI_COLORS["button_primary"])
        
        # Current turn info
        self.turn_info_label = tk.Label(
            self.frame,
            text="Game not started",
            font=FONTS["status"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_secondary"]
        )
        self.turn_info_label.pack(pady=5)
        
    def _handle_roll_dice(self):
        """Handle roll dice button click"""
        self.roll_button.config(state="disabled")
        self._animate_dice_roll()
        
        # Call the callback
        result = self.on_roll_dice()
        
        # Update button states based on result
        if result and result.get("success", False):
            if result.get("requires_action", False):
                self._enable_purchase_buttons()
            else:
                # Re-enable roll button for next player
                self.roll_button.config(state="normal")
    
    def _handle_buy_property(self):
        """Handle buy property button click"""
        result = self.on_buy_property()
        self._disable_purchase_buttons()
        self.roll_button.config(state="normal")
    
    def _handle_skip_purchase(self):
        """Handle skip purchase button click"""
        result = self.on_skip_purchase()
        self._disable_purchase_buttons()
        self.roll_button.config(state="normal")
    
    def _animate_dice_roll(self):
        """Animate dice rolling"""
        self.dice_result_label.config(text="Rolling...")
        self._show_random_dice()
        
        # Schedule final dice result after animation
        self.frame.after(ANIMATION["dice_roll_duration"], self._show_final_dice)
    
    def _show_random_dice(self, step=0):
        """Show random dice values during animation"""
        if step < 10:  # Animate for 10 steps
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            self._draw_dice(die1, die2)
            # Schedule next animation step
            self.frame.after(100, lambda: self._show_random_dice(step + 1))
    
    def _show_final_dice(self):
        """Show the final dice result"""
        # This will be called by update_dice_display with actual values
        pass
    
    def _draw_dice(self, die1: int, die2: int):
        """Draw enhanced dice on canvas with shadows and 3D effect"""
        self.dice_canvas.delete("all")
        
        # Draw shadows first (behind the dice)
        self._draw_die_shadow(17, 17, 20)  # Shadow for first die
        self._draw_die_shadow(67, 17, 20)  # Shadow for second die
        
        # Draw the actual dice
        self._draw_single_die(15, 15, 20, die1)
        self._draw_single_die(65, 15, 20, die2)
    
    def _draw_die_shadow(self, x: int, y: int, size: int):
        """Draw shadow behind die for 3D effect"""
        self.dice_canvas.create_rectangle(
            x, y, x + size, y + size,
            fill="#888888",
            outline="#666666",
            width=1
        )
    
    def _draw_single_die(self, x: int, y: int, size: int, value: int):
        """Draw a single die with enhanced 3D appearance and dots"""
        # Draw die background with gradient effect
        self.dice_canvas.create_rectangle(
            x, y, x + size, y + size,
            fill="#F8F8FF",  # Ghost white for clean look
            outline="#2F4F4F",  # Dark slate gray border
            width=2
        )
        
        # Add subtle inner border for 3D effect
        self.dice_canvas.create_rectangle(
            x + 1, y + 1, x + size - 1, y + size - 1,
            fill="",
            outline="#E6E6FA",  # Lavender highlight
            width=1
        )
        
        # Draw dots based on value with enhanced styling
        dot_size = 2.5
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Define dot color and shadow
        dot_color = "#2F4F4F"  # Dark slate gray
        dot_shadow = "#696969"  # Dim gray for shadow
        
        def draw_enhanced_dot(dot_x, dot_y):
            """Draw a single dot with shadow effect"""
            # Draw shadow slightly offset
            self.dice_canvas.create_oval(
                dot_x - dot_size + 0.5, dot_y - dot_size + 0.5,
                dot_x + dot_size + 0.5, dot_y + dot_size + 0.5,
                fill=dot_shadow, outline=""
            )
            # Draw main dot
            self.dice_canvas.create_oval(
                dot_x - dot_size, dot_y - dot_size,
                dot_x + dot_size, dot_y + dot_size,
                fill=dot_color, outline="#000000", width=0.5
            )
        
        if value == 1:
            draw_enhanced_dot(center_x, center_y)
        elif value == 2:
            draw_enhanced_dot(x + 6, y + 6)
            draw_enhanced_dot(x + size - 6, y + size - 6)
        elif value == 3:
            draw_enhanced_dot(x + 6, y + 6)
            draw_enhanced_dot(center_x, center_y)
            draw_enhanced_dot(x + size - 6, y + size - 6)
        elif value == 4:
            draw_enhanced_dot(x + 6, y + 6)
            draw_enhanced_dot(x + size - 6, y + 6)
            draw_enhanced_dot(x + 6, y + size - 6)
            draw_enhanced_dot(x + size - 6, y + size - 6)
        elif value == 5:
            draw_enhanced_dot(x + 6, y + 6)
            draw_enhanced_dot(x + size - 6, y + 6)
            draw_enhanced_dot(center_x, center_y)
            draw_enhanced_dot(x + 6, y + size - 6)
            draw_enhanced_dot(x + size - 6, y + size - 6)
        elif value == 6:
            draw_enhanced_dot(x + 6, y + 6)
            draw_enhanced_dot(x + size - 6, y + 6)
            draw_enhanced_dot(x + 6, center_y)
            draw_enhanced_dot(x + size - 6, center_y)
            draw_enhanced_dot(x + 6, y + size - 6)
            draw_enhanced_dot(x + size - 6, y + size - 6)
    
    def update_dice_display(self, die1: int, die2: int, total: int):
        """Update dice display with actual roll results"""
        self._draw_dice(die1, die2)
        self.dice_result_label.config(text=f"Rolled: {total}")
    
    def update_turn_info(self, current_player: str, phase: str):
        """Update turn information display"""
        phase_text = {
            "waiting_for_roll": "Click Roll Dice!",
            "rolled": "Processing move...",
            "action_required": "Choose an action",
            "turn_complete": "Turn complete"
        }
        
        info_text = f"{current_player}'s turn - {phase_text.get(phase, phase)}"
        self.turn_info_label.config(text=info_text)
    
    def _add_button_hover_effects(self, button, normal_color):
        """Add hover effects to button"""
        hover_color = lighten_color(normal_color, 0.9)
        
        def on_enter(event):
            if button['state'] == 'normal':
                button.config(bg=hover_color, relief="raised", bd=4)
        
        def on_leave(event):
            if button['state'] == 'normal':
                button.config(bg=normal_color, relief="raised", bd=3)
        
        def on_click(event):
            if button['state'] == 'normal':
                button.config(relief="sunken", bd=2)
                button.after(100, lambda: button.config(relief="raised", bd=3))
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)  
        button.bind("<Button-1>", on_click)
    
    def set_roll_enabled(self, enabled: bool):
        """Enable or disable roll dice button with enhanced visual feedback"""
        if enabled:
            self.roll_button.config(
                state="normal",
                bg=UI_COLORS["button_primary"],
                fg="white",
                cursor="hand2"
            )
        else:
            self.roll_button.config(
                state="disabled",
                bg=UI_COLORS["button_disabled"],
                fg=UI_COLORS["text_secondary"],
                cursor="arrow"
            )
    
    def _enable_purchase_buttons(self):
        """Enable purchase-related buttons with enhanced visual feedback"""
        self.buy_button.config(
            state="normal",
            bg=UI_COLORS["button_secondary"],
            fg="white",
            cursor="hand2"
        )
        self.skip_button.config(
            state="normal",
            bg=UI_COLORS["button_primary"],
            fg="white",
            cursor="hand2"
        )
    
    def _disable_purchase_buttons(self):
        """Disable purchase-related buttons with enhanced visual feedback"""
        self.buy_button.config(
            state="disabled",
            bg=UI_COLORS["button_disabled"],
            fg=UI_COLORS["text_secondary"],
            cursor="arrow"
        )
        self.skip_button.config(
            state="disabled",
            bg=UI_COLORS["button_disabled"],
            fg=UI_COLORS["text_secondary"],
            cursor="arrow"
        )
    
    def get_frame(self):
        """Return the main frame widget"""
        return self.frame

class PropertyDetailsPanel:
    """Panel showing current property information"""
    
    def __init__(self, parent):
        """Initialize property details panel"""
        self.parent = parent
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=UI_COLORS["panel_background"], relief="raised", bd=2)
        
        # Title
        title = tk.Label(
            self.frame,
            text="PROPERTY INFO",
            font=FONTS["title"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        )
        title.pack(pady=5)
        
        # Property info container
        self.info_frame = tk.Frame(self.frame, bg=UI_COLORS["panel_background"])
        self.info_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Property name
        self.name_label = tk.Label(
            self.info_frame,
            text="No property selected",
            font=FONTS["player"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"],
            wraplength=180
        )
        self.name_label.pack(pady=5)
        
        # Property details
        self.details_text = tk.Text(
            self.info_frame,
            height=8,
            width=25,
            font=FONTS["status"],
            bg=UI_COLORS["background"],
            fg=UI_COLORS["text_primary"],
            relief="sunken",
            bd=1,
            state="disabled"
        )
        self.details_text.pack(fill="both", expand=True)
        
    def update_property_info(self, property_data: Dict):
        """Update property information display with comprehensive details"""
        if not property_data:
            self.name_label.config(text="No property selected")
            self._update_details_text("Click on a property to see details")
            return
        
        # Update property name
        property_name = property_data.get("name", "Unknown")
        self.name_label.config(text=property_name)
        
        # Build comprehensive details text
        details = []
        
        # Property type and basic info
        property_type = self._determine_property_type(property_name, property_data.get("color_group", "N/A"))
        details.append(f"Type: {property_type}")
        
        # Purchase cost
        cost = property_data.get("cost", "N/A")
        if cost != "N/A":
            details.append(f"Purchase Cost: ${cost}")
            
            # Mortgage value (usually half of cost)
            try:
                mortgage_value = int(cost) // 2
                details.append(f"Mortgage Value: ${mortgage_value}")
            except (ValueError, TypeError):
                pass
        
        # Color group information
        color_group = property_data.get("color_group", "N/A")
        if color_group != "N/A":
            details.append(f"Color Group: {color_group}")
            
            # Group completion info
            group_properties = self._get_group_property_count(color_group)
            if group_properties:
                details.append(f"Properties in group: {group_properties}")
        
        # Ownership information
        owner = property_data.get("owner", "Bank")
        if owner == "Bank":
            details.append("\n🏛️ AVAILABLE FOR PURCHASE")
        else:
            details.append(f"\n👤 Owner: {owner}")
            
            # Property status
            if property_data.get("mortgaged", False):
                details.append("📋 Status: MORTGAGED")
            else:
                details.append("📋 Status: Active")
        
        # Development information
        houses = property_data.get("houses", 0)
        if isinstance(houses, int) and houses > 0:
            details.append("\n🏗️ DEVELOPMENT:")
            if houses == 5:
                details.append("🏨 Hotel built")
            else:
                house_text = "house" if houses == 1 else "houses"
                details.append(f"🏠 {houses} {house_text} built")
        
        # Rent structure
        rent_info = property_data.get("rent", {})
        if rent_info and isinstance(rent_info, dict):
            details.append("\n💰 RENT STRUCTURE:")
            rent_items = sorted(rent_info.items()) if isinstance(rent_info, dict) else []
            
            for houses_count, rent_amount in rent_items:
                if houses_count == 0:
                    details.append(f"  Base rent: ${rent_amount}")
                elif houses_count == 1:
                    details.append(f"  With 1 house: ${rent_amount}")
                elif houses_count == 2:
                    details.append(f"  With 2 houses: ${rent_amount}")
                elif houses_count == 3:
                    details.append(f"  With 3 houses: ${rent_amount}")
                elif houses_count == 4:
                    details.append(f"  With 4 houses: ${rent_amount}")
                elif houses_count == 5:
                    details.append(f"  With hotel: ${rent_amount}")
        
        # Special property information
        if property_type == "Railroad":
            details.append("\n🚂 RAILROAD SPECIAL RULES:")
            details.append("  Rent depends on # owned:")
            details.append("  1 railroad: $25")
            details.append("  2 railroads: $50") 
            details.append("  3 railroads: $100")
            details.append("  4 railroads: $200")
        elif property_type == "Utility":
            details.append("\n⚡ UTILITY SPECIAL RULES:")
            details.append("  Rent = dice roll × multiplier")
            details.append("  1 utility: 4× dice roll")
            details.append("  2 utilities: 10× dice roll")
        
        self._update_details_text("\n".join(details))
    
    def _determine_property_type(self, name: str, color_group: str) -> str:
        """Determine the display type of property"""
        name_upper = name.upper()
        if "RAILROAD" in name_upper:
            return "Railroad"
        elif "ELECTRIC" in name_upper or "WATER" in name_upper:
            return "Utility"
        elif "TAX" in name_upper:
            return "Tax Space"
        elif "CHANCE" in name_upper:
            return "Chance"
        elif "COMMUNITY CHEST" in name_upper:
            return "Community Chest"
        elif name_upper in ["GO", "JAIL", "FREE PARKING", "GO TO JAIL"]:
            return "Special Space"
        else:
            return "Property"
    
    def _get_group_property_count(self, color_group: str) -> str:
        """Get the number of properties in a color group"""
        group_counts = {
            "Brown": "2 properties",
            "Light Blue": "3 properties",
            "Pink": "3 properties", 
            "Orange": "3 properties",
            "Red": "3 properties",
            "Yellow": "3 properties",
            "Green": "3 properties",
            "Blue": "2 properties",
            "Railroad": "4 railroads",
            "Utilities": "2 utilities"
        }
        return group_counts.get(color_group, "")
    
    def _update_details_text(self, text: str):
        """Update the details text widget"""
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", text)
        self.details_text.config(state="disabled")
    
    def get_frame(self):
        """Return the main frame widget"""
        return self.frame

class GameLogPanel:
    """Panel showing game events and history"""
    
    def __init__(self, parent):
        """Initialize game log panel"""
        self.parent = parent
        self.max_events = 50  # Maximum number of events to keep
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=UI_COLORS["panel_background"], relief="raised", bd=2)
        
        # Title
        title = tk.Label(
            self.frame,
            text="GAME LOG",
            font=FONTS["title"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        )
        title.pack(pady=5)
        
        # Log display with scrollbar
        log_frame = tk.Frame(self.frame)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Text widget
        self.log_text = tk.Text(
            log_frame,
            height=12,
            width=30,
            font=FONTS["status"],
            bg=UI_COLORS["background"],
            fg=UI_COLORS["text_primary"],
            relief="sunken",
            bd=1,
            state="disabled",
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.log_text.yview)
        
        # Clear log button
        clear_button = tk.Button(
            self.frame,
            text="Clear Log",
            font=("Arial", 9),
            bg=UI_COLORS["button_disabled"],
            fg=UI_COLORS["text_secondary"],
            command=self.clear_log,
            relief="flat"
        )
        clear_button.pack(pady=5)
        
        # Initialize with welcome message
        self.add_event("Welcome to Monopoly! Start the game to begin.", "system")
    
    def add_event(self, message: str, event_type: str = "info"):
        """
        Add an event to the log
        :param message: Event message
        :param event_type: Type of event (info, success, error, system)
        """
        # Determine text color based on event type
        colors = {
            "info": UI_COLORS["text_primary"],
            "success": UI_COLORS["text_success"],
            "error": UI_COLORS["text_error"],
            "system": UI_COLORS["text_secondary"],
            "highlight": UI_COLORS["text_highlight"]
        }
        
        color = colors.get(event_type, UI_COLORS["text_primary"])
        
        # Enable text widget for editing
        self.log_text.config(state="normal")
        
        # Add timestamp prefix
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Insert the message
        self.log_text.insert(tk.END, formatted_message)
        
        # Apply color formatting (simplified - using tags would be more complex)
        # For now, we'll keep it simple with consistent coloring
        
        # Auto-scroll to bottom
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = int(self.log_text.index(tk.END).split('.')[0])
        if lines > self.max_events:
            # Remove oldest entries
            excess = lines - self.max_events
            self.log_text.delete("1.0", f"{excess}.0")
        
        # Disable text widget
        self.log_text.config(state="disabled")
    
    def clear_log(self):
        """Clear all log entries"""
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")
        self.add_event("Log cleared.", "system")
    
    def get_frame(self):
        """Return the main frame widget"""
        return self.frame