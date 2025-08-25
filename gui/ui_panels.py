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
        """Highlight the current player"""
        # Hide all current indicators
        for widgets in self.player_widgets.values():
            widgets["current_indicator"].pack_forget()
        
        # Show indicator for current player
        if player_name in self.player_widgets:
            self.player_widgets[player_name]["current_indicator"].pack(side="right")
    
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
        
        # Roll Dice button
        self.roll_button = tk.Button(
            self.buttons_frame,
            text="🎲 ROLL DICE",
            font=FONTS["button"],
            bg=UI_COLORS["button_primary"],
            fg="white",
            relief="raised",
            bd=3,
            command=self._handle_roll_dice,
            cursor="hand2"
        )
        self.roll_button.pack(fill="x", pady=2)
        
        # Buy Property button
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
            state="disabled"
        )
        self.buy_button.pack(fill="x", pady=2)
        
        # Skip Purchase button
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
            state="disabled"
        )
        self.skip_button.pack(fill="x", pady=2)
        
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
        """Draw dice on canvas"""
        self.dice_canvas.delete("all")
        
        # Draw first die
        self._draw_single_die(15, 15, 20, die1)
        
        # Draw second die  
        self._draw_single_die(65, 15, 20, die2)
    
    def _draw_single_die(self, x: int, y: int, size: int, value: int):
        """Draw a single die with dots"""
        # Draw die background
        self.dice_canvas.create_rectangle(
            x, y, x + size, y + size,
            fill="white",
            outline="black",
            width=2
        )
        
        # Draw dots based on value
        dot_size = 3
        center_x = x + size // 2
        center_y = y + size // 2
        
        if value == 1:
            self.dice_canvas.create_oval(center_x - dot_size, center_y - dot_size, 
                                       center_x + dot_size, center_y + dot_size, fill="black")
        elif value == 2:
            self.dice_canvas.create_oval(x + 5, y + 5, x + 8, y + 8, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + size - 8, x + size - 5, y + size - 5, fill="black")
        elif value == 3:
            self.dice_canvas.create_oval(x + 5, y + 5, x + 8, y + 8, fill="black")
            self.dice_canvas.create_oval(center_x - 1, center_y - 1, center_x + 2, center_y + 2, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + size - 8, x + size - 5, y + size - 5, fill="black")
        elif value == 4:
            self.dice_canvas.create_oval(x + 5, y + 5, x + 8, y + 8, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + 5, x + size - 5, y + 8, fill="black")
            self.dice_canvas.create_oval(x + 5, y + size - 8, x + 8, y + size - 5, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + size - 8, x + size - 5, y + size - 5, fill="black")
        elif value == 5:
            self.dice_canvas.create_oval(x + 5, y + 5, x + 8, y + 8, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + 5, x + size - 5, y + 8, fill="black")
            self.dice_canvas.create_oval(center_x - 1, center_y - 1, center_x + 2, center_y + 2, fill="black")
            self.dice_canvas.create_oval(x + 5, y + size - 8, x + 8, y + size - 5, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + size - 8, x + size - 5, y + size - 5, fill="black")
        elif value == 6:
            self.dice_canvas.create_oval(x + 5, y + 5, x + 8, y + 8, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + 5, x + size - 5, y + 8, fill="black")
            self.dice_canvas.create_oval(x + 5, center_y - 1, x + 8, center_y + 2, fill="black")
            self.dice_canvas.create_oval(x + size - 8, center_y - 1, x + size - 5, center_y + 2, fill="black")
            self.dice_canvas.create_oval(x + 5, y + size - 8, x + 8, y + size - 5, fill="black")
            self.dice_canvas.create_oval(x + size - 8, y + size - 8, x + size - 5, y + size - 5, fill="black")
    
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
    
    def set_roll_enabled(self, enabled: bool):
        """Enable or disable roll dice button"""
        state = "normal" if enabled else "disabled"
        self.roll_button.config(state=state)
        
        if enabled:
            self.roll_button.config(bg=UI_COLORS["button_primary"])
        else:
            self.roll_button.config(bg=UI_COLORS["button_disabled"])
    
    def _enable_purchase_buttons(self):
        """Enable purchase-related buttons"""
        self.buy_button.config(
            state="normal",
            bg=UI_COLORS["button_secondary"]
        )
        self.skip_button.config(
            state="normal",
            bg=UI_COLORS["button_primary"]
        )
    
    def _disable_purchase_buttons(self):
        """Disable purchase-related buttons"""
        self.buy_button.config(
            state="disabled",
            bg=UI_COLORS["button_disabled"]
        )
        self.skip_button.config(
            state="disabled",
            bg=UI_COLORS["button_disabled"]
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
        """Update property information display"""
        if not property_data:
            self.name_label.config(text="No property selected")
            self._update_details_text("Click on a property to see details")
            return
        
        # Update property name
        self.name_label.config(text=property_data.get("name", "Unknown"))
        
        # Build details text
        details = []
        
        if property_data.get("cost") != "N/A":
            details.append(f"Cost: ${property_data.get('cost', 0)}")
        
        color_group = property_data.get("color_group", "N/A")
        if color_group != "N/A":
            details.append(f"Group: {color_group}")
        
        owner = property_data.get("owner", "Bank")
        if owner == "Bank":
            details.append("Owner: Available for purchase")
        else:
            details.append(f"Owner: {owner}")
        
        if property_data.get("mortgaged", False):
            details.append("Status: MORTGAGED")
        
        rent_info = property_data.get("rent", {})
        if rent_info and isinstance(rent_info, dict):
            details.append("\nRent:")
            for houses, rent in rent_info.items():
                if houses == 0:
                    details.append(f"  Base: ${rent}")
                elif houses == 5:
                    details.append(f"  Hotel: ${rent}")
                else:
                    details.append(f"  {houses} houses: ${rent}")
        
        houses = property_data.get("houses", 0)
        if houses > 0:
            if houses == 5:
                details.append(f"\n🏨 Hotel built")
            else:
                details.append(f"\n🏠 {houses} house{'s' if houses != 1 else ''}")
        
        self._update_details_text("\n".join(details))
    
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