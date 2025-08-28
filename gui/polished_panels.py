"""
@author: Aleph Aseffa
Polished UI Panels for Monopoly

Professional-grade UI components with authentic Monopoly aesthetics
and smooth interactions
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable, Any
import random
import datetime
import colors

class MonopolyPlayerPanel:
    """
    Professional player information panel with Monopoly styling
    """
    
    def __init__(self, parent: tk.Widget, players_data: List[Dict]):
        """Initialize player panel with authentic design"""
        self.parent = parent
        self.players_data = players_data
        
        # Create main frame with Monopoly styling
        self.frame = tk.Frame(
            parent,
            bg=colors.UI_COLORS["panel_background"],
            relief="raised",
            bd=2
        )
        
        # Title bar
        self._create_title_bar()
        
        # Player cards container
        self.players_container = tk.Frame(
            self.frame,
            bg=colors.UI_COLORS["panel_background"]
        )
        self.players_container.pack(fill="both", expand=True, padx=8, pady=5)
        
        # Store player card widgets
        self.player_cards = {}
        
        # Create player cards
        for i, player_data in enumerate(players_data):
            self._create_player_card(i, player_data)
    
    def _create_title_bar(self):
        """Create professional title bar"""
        title_frame = tk.Frame(
            self.frame,
            bg=colors.BOARD_COLORS["go_background"],
            height=35
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="PLAYERS",
            font=colors.FONTS["title_medium"],
            bg=colors.BOARD_COLORS["go_background"],
            fg="white"
        )
        title.place(relx=0.5, rely=0.5, anchor="center")
    
    def _create_player_card(self, index: int, player_data: Dict):
        """Create a polished player card"""
        player_name = player_data["name"]
        player_color = colors.get_player_color(index)
        
        # Card frame
        card = tk.Frame(
            self.players_container,
            bg="white",
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        card.pack(fill="x", pady=4)
        
        # Color indicator bar
        color_bar = tk.Frame(
            card,
            bg=player_color,
            height=4
        )
        color_bar.pack(fill="x")
        
        # Content frame
        content = tk.Frame(card, bg="white", padx=10, pady=8)
        content.pack(fill="x")
        
        # Player name with token
        name_frame = tk.Frame(content, bg="white")
        name_frame.pack(fill="x")
        
        # Token indicator
        token_canvas = tk.Canvas(
            name_frame,
            width=20, height=20,
            bg="white",
            highlightthickness=0
        )
        token_canvas.pack(side="left", padx=(0, 8))
        
        token_canvas.create_oval(
            3, 3, 17, 17,
            fill=player_color,
            outline=colors.darken_color(player_color, 0.6),
            width=2
        )
        
        # Player name
        name_label = tk.Label(
            name_frame,
            text=player_name,
            font=colors.FONTS["player_name"],
            bg="white",
            fg=colors.UI_COLORS["text_primary"]
        )
        name_label.pack(side="left")
        
        # Turn indicator (initially hidden)
        turn_indicator = tk.Label(
            name_frame,
            text="◀ YOUR TURN",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=colors.BOARD_COLORS["go_background"]
        )
        turn_indicator.pack(side="right")
        turn_indicator.pack_forget()
        
        # Stats frame
        stats_frame = tk.Frame(content, bg="white")
        stats_frame.pack(fill="x", pady=(5, 0))
        
        # Balance with money icon
        balance_frame = tk.Frame(stats_frame, bg="white")
        balance_frame.pack(fill="x")
        
        balance_label = tk.Label(
            balance_frame,
            text=f"💰 ${player_data['balance']:,}",
            font=colors.FONTS["money_amount"],
            bg="white",
            fg=colors.UI_COLORS["text_success"]
        )
        balance_label.pack(side="left")
        
        # Properties count
        properties_label = tk.Label(
            stats_frame,
            text=f"Properties: {player_data['properties']}",
            font=colors.FONTS["player_info"],
            bg="white",
            fg=colors.UI_COLORS["text_secondary"]
        )
        properties_label.pack(anchor="w")
        
        # Status badges
        status_frame = tk.Frame(stats_frame, bg="white")
        status_frame.pack(fill="x", pady=(2, 0))
        
        # Jail badge (initially hidden)
        jail_badge = tk.Label(
            status_frame,
            text="🔒 IN JAIL",
            font=("Arial", 9, "bold"),
            bg=colors.BOARD_COLORS["jail_background"],
            fg="white",
            padx=5,
            pady=2
        )
        jail_badge.pack(side="left")
        jail_badge.pack_forget()
        
        # Bankrupt badge (initially hidden)
        bankrupt_badge = tk.Label(
            status_frame,
            text="❌ BANKRUPT",
            font=("Arial", 9, "bold"),
            bg=colors.UI_COLORS["text_error"],
            fg="white",
            padx=5,
            pady=2
        )
        bankrupt_badge.pack(side="left")
        bankrupt_badge.pack_forget()
        
        # Store references
        self.player_cards[player_name] = {
            "card": card,
            "name_label": name_label,
            "turn_indicator": turn_indicator,
            "balance_label": balance_label,
            "properties_label": properties_label,
            "jail_badge": jail_badge,
            "bankrupt_badge": bankrupt_badge,
            "color": player_color
        }
    
    def update_player(self, player_name: str, data: Dict):
        """Update player information"""
        if player_name not in self.player_cards:
            return
        
        widgets = self.player_cards[player_name]
        
        # Update balance
        balance = data.get("balance", 0)
        widgets["balance_label"].config(text=f"💰 ${balance:,}")
        
        # Update properties
        properties = data.get("properties", 0)
        widgets["properties_label"].config(text=f"Properties: {properties}")
        
        # Update status badges
        if data.get("in_jail", False):
            widgets["jail_badge"].pack(side="left", padx=2)
        else:
            widgets["jail_badge"].pack_forget()
        
        if data.get("bankrupt", False):
            widgets["bankrupt_badge"].pack(side="left", padx=2)
            widgets["card"].config(bg="#F0F0F0")
        else:
            widgets["bankrupt_badge"].pack_forget()
    
    def set_current_player(self, player_name: str):
        """Highlight current player"""
        for name, widgets in self.player_cards.items():
            if name == player_name:
                widgets["turn_indicator"].pack(side="right")
                widgets["card"].config(relief="raised", bd=3)
            else:
                widgets["turn_indicator"].pack_forget()
                widgets["card"].config(relief="solid", bd=1)
    
    def get_frame(self) -> tk.Frame:
        """Get the main frame"""
        return self.frame


class MonopolyControlPanel:
    """
    Professional game control panel with authentic Monopoly styling
    """
    
    def __init__(self, parent: tk.Widget, callbacks: Dict[str, Callable]):
        """Initialize control panel"""
        self.parent = parent
        self.callbacks = callbacks
        
        # Create main frame
        self.frame = tk.Frame(
            parent,
            bg=colors.UI_COLORS["panel_background"],
            relief="raised",
            bd=2
        )
        
        # Title bar
        self._create_title_bar()
        
        # Content container
        content = tk.Frame(
            self.frame,
            bg=colors.UI_COLORS["panel_background"],
            padx=10,
            pady=10
        )
        content.pack(fill="both", expand=True)
        
        # Dice display
        self._create_dice_display(content)
        
        # Action buttons
        self._create_action_buttons(content)
        
        # Turn information
        self._create_turn_info(content)
        
        # Animation state
        self.dice_animation = None
    
    def _create_title_bar(self):
        """Create title bar"""
        title_frame = tk.Frame(
            self.frame,
            bg=colors.BOARD_COLORS["go_background"],
            height=35
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="GAME CONTROLS",
            font=colors.FONTS["title_medium"],
            bg=colors.BOARD_COLORS["go_background"],
            fg="white"
        )
        title.place(relx=0.5, rely=0.5, anchor="center")
    
    def _create_dice_display(self, parent):
        """Create dice display area"""
        dice_frame = tk.LabelFrame(
            parent,
            text="DICE",
            font=colors.FONTS["title_small"],
            bg=colors.UI_COLORS["panel_background"],
            fg=colors.UI_COLORS["text_primary"],
            relief="groove",
            bd=2
        )
        dice_frame.pack(fill="x", pady=(0, 10))
        
        # Dice canvas
        self.dice_canvas = tk.Canvas(
            dice_frame,
            width=120, height=60,
            bg="white",
            highlightthickness=0
        )
        self.dice_canvas.pack(pady=10)
        
        # Result label
        self.dice_result = tk.Label(
            dice_frame,
            text="Ready to roll!",
            font=colors.FONTS["dice_number"],
            bg=colors.UI_COLORS["panel_background"],
            fg=colors.UI_COLORS["text_primary"]
        )
        self.dice_result.pack(pady=(0, 10))
        
        # Draw initial dice
        self._draw_dice(1, 1)
    
    def _draw_dice(self, die1: int, die2: int):
        """Draw dice with professional styling"""
        self.dice_canvas.delete("all")
        
        # Die 1
        self._draw_single_die(20, 10, die1)
        
        # Die 2
        self._draw_single_die(70, 10, die2)
    
    def _draw_single_die(self, x: int, y: int, value: int):
        """Draw a single die"""
        size = 40
        
        # Die background
        self.dice_canvas.create_rectangle(
            x, y, x + size, y + size,
            fill="white",
            outline="black",
            width=2
        )
        
        # Draw dots
        dot_positions = {
            1: [(20, 20)],
            2: [(10, 10), (30, 30)],
            3: [(10, 10), (20, 20), (30, 30)],
            4: [(10, 10), (30, 10), (10, 30), (30, 30)],
            5: [(10, 10), (30, 10), (20, 20), (10, 30), (30, 30)],
            6: [(10, 10), (30, 10), (10, 20), (30, 20), (10, 30), (30, 30)]
        }
        
        for dx, dy in dot_positions.get(value, []):
            self.dice_canvas.create_oval(
                x + dx - 3, y + dy - 3,
                x + dx + 3, y + dy + 3,
                fill="black"
            )
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(
            parent,
            bg=colors.UI_COLORS["panel_background"]
        )
        buttons_frame.pack(fill="x", pady=10)
        
        # Roll dice button
        self.roll_button = self._create_button(
            buttons_frame,
            "🎲 ROLL DICE",
            colors.UI_COLORS["button_primary"],
            self.callbacks.get("on_roll_dice", lambda: None)
        )
        self.roll_button.pack(fill="x", pady=3)
        
        # Buy property button
        self.buy_button = self._create_button(
            buttons_frame,
            "💰 BUY PROPERTY",
            colors.UI_COLORS["button_secondary"],
            self.callbacks.get("on_buy_property", lambda: None)
        )
        self.buy_button.pack(fill="x", pady=3)
        self.buy_button.config(state="disabled")
        
        # Skip purchase button
        self.skip_button = self._create_button(
            buttons_frame,
            "⏭️ SKIP PURCHASE",
            colors.UI_COLORS["button_warning"],
            self.callbacks.get("on_skip_purchase", lambda: None)
        )
        self.skip_button.pack(fill="x", pady=3)
        self.skip_button.config(state="disabled")
    
    def _create_button(self, parent, text: str, color: str, command: Callable) -> tk.Button:
        """Create a styled button"""
        button = tk.Button(
            parent,
            text=text,
            font=colors.FONTS["button_text"],
            bg=color,
            fg=colors.UI_COLORS["button_text"],
            relief="raised",
            bd=2,
            cursor="hand2",
            command=command,
            activebackground=colors.darken_color(color, 0.9)
        )
        
        # Add hover effects
        button.bind("<Enter>", lambda e: button.config(bg=lighten_color(color, 0.2)))
        button.bind("<Leave>", lambda e: button.config(bg=color))
        
        return button
    
    def _create_turn_info(self, parent):
        """Create turn information display"""
        self.turn_info = tk.Label(
            parent,
            text="Game not started",
            font=colors.FONTS["status_text"],
            bg=colors.UI_COLORS["panel_background"],
            fg=colors.UI_COLORS["text_secondary"],
            wraplength=200
        )
        self.turn_info.pack(pady=10)
    
    def animate_dice_roll(self):
        """Animate dice rolling"""
        self.dice_result.config(text="Rolling...")
        self._animate_dice(0)
    
    def _animate_dice(self, count: int):
        """Dice animation step"""
        if count < 10:
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            self._draw_dice(die1, die2)
            self.dice_canvas.after(100, lambda: self._animate_dice(count + 1))
    
    def show_dice_result(self, die1: int, die2: int):
        """Show final dice result"""
        self._draw_dice(die1, die2)
        total = die1 + die2
        self.dice_result.config(text=f"Rolled: {total}")
        
        if die1 == die2:
            self.dice_result.config(text=f"DOUBLES! {total}")
    
    def update_turn_info(self, text: str):
        """Update turn information"""
        self.turn_info.config(text=text)
    
    def enable_roll(self, enabled: bool = True):
        """Enable/disable roll button"""
        self.roll_button.config(
            state="normal" if enabled else "disabled",
            bg=colors.UI_COLORS["button_primary"] if enabled else colors.UI_COLORS["button_disabled"]
        )
    
    def enable_purchase_buttons(self, enabled: bool = True):
        """Enable/disable purchase buttons"""
        state = "normal" if enabled else "disabled"
        
        self.buy_button.config(
            state=state,
            bg=colors.UI_COLORS["button_secondary"] if enabled else colors.UI_COLORS["button_disabled"]
        )
        
        self.skip_button.config(
            state=state,
            bg=colors.UI_COLORS["button_warning"] if enabled else colors.UI_COLORS["button_disabled"]
        )
    
    def get_frame(self) -> tk.Frame:
        """Get the main frame"""
        return self.frame


class MonopolyPropertyCard:
    """
    Property information card with authentic Monopoly design
    """
    
    def __init__(self, parent: tk.Widget):
        """Initialize property card"""
        self.parent = parent
        
        # Create main frame
        self.frame = tk.Frame(
            parent,
            bg=colors.UI_COLORS["panel_background"],
            relief="raised",
            bd=2
        )
        
        # Title bar
        self._create_title_bar()
        
        # Card display area
        self.card_container = tk.Frame(
            self.frame,
            bg=colors.UI_COLORS["panel_background"],
            padx=10,
            pady=10
        )
        self.card_container.pack(fill="both", expand=True)
        
        # Property card
        self.property_card = tk.Frame(
            self.card_container,
            bg="white",
            relief="solid",
            bd=2
        )
        self.property_card.pack(fill="both", expand=True)
        
        # Initialize with no property
        self._show_no_property()
    
    def _create_title_bar(self):
        """Create title bar"""
        title_frame = tk.Frame(
            self.frame,
            bg=colors.BOARD_COLORS["go_background"],
            height=35
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="PROPERTY CARD",
            font=colors.FONTS["title_medium"],
            bg=colors.BOARD_COLORS["go_background"],
            fg="white"
        )
        title.place(relx=0.5, rely=0.5, anchor="center")
    
    def _show_no_property(self):
        """Show no property selected state"""
        # Clear card
        for widget in self.property_card.winfo_children():
            widget.destroy()
        
        # Message
        msg = tk.Label(
            self.property_card,
            text="Click on a property\nto view details",
            font=colors.FONTS["player_info"],
            bg="white",
            fg=colors.UI_COLORS["text_tertiary"],
            justify="center"
        )
        msg.place(relx=0.5, rely=0.5, anchor="center")
    
    def show_property(self, property_data: Dict):
        """Display property information"""
        # Clear card
        for widget in self.property_card.winfo_children():
            widget.destroy()
        
        if not property_data:
            self._show_no_property()
            return
        
        # Get property details
        name = property_data.get("name", "Unknown")
        color_group = property_data.get("color_group", "")
        cost = property_data.get("cost", "N/A")
        owner = property_data.get("owner", "Bank")
        
        # Color bar for colored properties
        if self._is_colored_property(color_group):
            color_bar = tk.Frame(
                self.property_card,
                bg=get_property_color(color_group),
                height=30
            )
            color_bar.pack(fill="x")
        
        # Property name
        name_label = tk.Label(
            self.property_card,
            text=name.upper(),
            font=colors.FONTS["title_small"],
            bg="white",
            fg=colors.UI_COLORS["text_primary"]
        )
        name_label.pack(pady=10)
        
        # Content frame
        content = tk.Frame(self.property_card, bg="white", padx=15)
        content.pack(fill="both", expand=True, pady=10)
        
        # Ownership
        owner_frame = tk.Frame(content, bg="white")
        owner_frame.pack(fill="x", pady=5)
        
        tk.Label(
            owner_frame,
            text="Owner:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=colors.UI_COLORS["text_secondary"]
        ).pack(side="left")
        
        tk.Label(
            owner_frame,
            text=owner if owner != "Bank" else "Available",
            font=("Arial", 10),
            bg="white",
            fg=colors.UI_COLORS["text_success"] if owner == "Bank" else colors.UI_COLORS["text_primary"]
        ).pack(side="left", padx=(5, 0))
        
        # Cost
        if cost != "N/A":
            cost_frame = tk.Frame(content, bg="white")
            cost_frame.pack(fill="x", pady=5)
            
            tk.Label(
                cost_frame,
                text="Cost:",
                font=("Arial", 10, "bold"),
                bg="white",
                fg=colors.UI_COLORS["text_secondary"]
            ).pack(side="left")
            
            tk.Label(
                cost_frame,
                text=f"${cost}",
                font=colors.FONTS["money_amount"],
                bg="white",
                fg=colors.UI_COLORS["text_primary"]
            ).pack(side="left", padx=(5, 0))
        
        # Rent information
        rent_info = property_data.get("rent", {})
        if rent_info:
            tk.Label(
                content,
                text="RENT",
                font=("Arial", 10, "bold"),
                bg="white",
                fg=colors.UI_COLORS["text_secondary"]
            ).pack(pady=(10, 5))
            
            rent_frame = tk.Frame(content, bg="white")
            rent_frame.pack(fill="x")
            
            # Display rent tiers
            rent_labels = [
                "Base rent:", "1 House:", "2 Houses:",
                "3 Houses:", "4 Houses:", "Hotel:"
            ]
            
            for i, label in enumerate(rent_labels):
                if i in rent_info:
                    row = tk.Frame(rent_frame, bg="white")
                    row.pack(fill="x", pady=1)
                    
                    tk.Label(
                        row,
                        text=label,
                        font=("Arial", 9),
                        bg="white",
                        fg=colors.UI_COLORS["text_secondary"],
                        width=10,
                        anchor="w"
                    ).pack(side="left")
                    
                    tk.Label(
                        row,
                        text=f"${rent_info[i]}",
                        font=("Arial", 9, "bold"),
                        bg="white",
                        fg=colors.UI_COLORS["text_primary"]
                    ).pack(side="left")
    
    def _is_colored_property(self, color_group: str) -> bool:
        """Check if this is a colored property"""
        return color_group in colors.PROPERTY_COLORS and color_group not in ["Railroad", "Utilities"]
    
    def get_frame(self) -> tk.Frame:
        """Get the main frame"""
        return self.frame


class MonopolyGameLog:
    """
    Game event log with professional styling
    """
    
    def __init__(self, parent: tk.Widget):
        """Initialize game log"""
        self.parent = parent
        
        # Create main frame
        self.frame = tk.Frame(
            parent,
            bg=colors.UI_COLORS["panel_background"],
            relief="raised",
            bd=2
        )
        
        # Title bar
        self._create_title_bar()
        
        # Log area
        log_container = tk.Frame(
            self.frame,
            bg=colors.UI_COLORS["panel_background"],
            padx=5,
            pady=5
        )
        log_container.pack(fill="both", expand=True)
        
        # Scrollable text widget
        scroll_frame = tk.Frame(log_container)
        scroll_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            scroll_frame,
            height=10,
            font=colors.FONTS["log_text"],
            bg="white",
            fg=colors.UI_COLORS["text_primary"],
            wrap="word",
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.log_text.yview)
        
        # Configure text tags for different message types
        self.log_text.tag_config("info", foreground=colors.UI_COLORS["text_info"])
        self.log_text.tag_config("success", foreground=colors.UI_COLORS["text_success"])
        self.log_text.tag_config("warning", foreground=colors.UI_COLORS["text_warning"])
        self.log_text.tag_config("error", foreground=colors.UI_COLORS["text_error"])
        self.log_text.tag_config("timestamp", foreground=colors.UI_COLORS["text_tertiary"])
        
        # Clear button
        clear_btn = tk.Button(
            log_container,
            text="Clear Log",
            font=("Arial", 9),
            bg=colors.UI_COLORS["button_disabled"],
            fg=colors.UI_COLORS["text_secondary"],
            relief="flat",
            command=self.clear_log
        )
        clear_btn.pack(pady=5)
        
        # Add welcome message
        self.add_event("Welcome to Monopoly!", "success")
    
    def _create_title_bar(self):
        """Create title bar"""
        title_frame = tk.Frame(
            self.frame,
            bg=colors.BOARD_COLORS["go_background"],
            height=35
        )
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="GAME LOG",
            font=colors.FONTS["title_medium"],
            bg=colors.BOARD_COLORS["go_background"],
            fg="white"
        )
        title.place(relx=0.5, rely=0.5, anchor="center")
    
    def add_event(self, message: str, event_type: str = "info"):
        """Add an event to the log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.log_text.config(state="normal")
        
        # Add timestamp
        self.log_text.insert("end", f"[{timestamp}] ", "timestamp")
        
        # Add message
        self.log_text.insert("end", f"{message}\n", event_type)
        
        # Auto-scroll to bottom
        self.log_text.see("end")
        
        self.log_text.config(state="disabled")
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
        
        self.add_event("Log cleared", "info")
    
    def get_frame(self) -> tk.Frame:
        """Get the main frame"""
        return self.frame