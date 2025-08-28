"""
@author: Aleph Aseffa
Polished Monopoly GUI Application

Main application window that integrates all polished UI components
into a professional, authentic Monopoly game interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .colors import *
from .authentic_board import AuthenticMonopolyBoard
from .polished_panels import (
    MonopolyPlayerPanel,
    MonopolyControlPanel,
    MonopolyPropertyCard,
    MonopolyGameLog
)
from .game_controller import GameController


class PolishedMonopolyGUI:
    """
    Professional Monopoly GUI with authentic design and smooth interactions
    """
    
    def __init__(self):
        """Initialize the polished Monopoly GUI"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("MONOPOLY - Property Trading Game")
        self.root.geometry(f"{SIZES['window_width']}x{SIZES['window_height']}")
        self.root.configure(bg=UI_COLORS["app_background"])
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/monopoly_icon.ico")
        except:
            pass  # Icon file not found
        
        # Initialize game controller
        self.game_controller = GameController()
        self._setup_game_callbacks()
        
        # Create UI layout
        self._create_menu_bar()
        self._create_main_layout()
        
        # Initialize game state
        self.game_state = {
            "started": False,
            "current_player": None,
            "turn_phase": "waiting",
            "dice_rolled": False
        }
        
        # Center window on screen
        self._center_window()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Show welcome screen
        self._show_welcome_screen()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position
        self.root.geometry(f"+{x}+{y}")
    
    def _create_menu_bar(self):
        """Create professional menu bar"""
        menubar = tk.Menu(self.root, bg="white", fg=UI_COLORS["text_primary"])
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self._start_new_game,
                             accelerator="Ctrl+N")
        game_menu.add_command(label="Reset Game", command=self._reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Settings", command=self._show_settings)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self._on_closing,
                             accelerator="Alt+F4")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Show Property Values")
        view_menu.add_checkbutton(label="Show Player Stats")
        view_menu.add_separator()
        view_menu.add_command(label="Zoom In", accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", accelerator="Ctrl+0")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Play", command=self._show_help)
        help_menu.add_command(label="Monopoly Rules", command=self._show_rules)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self._start_new_game())
    
    def _create_main_layout(self):
        """Create the main application layout"""
        # Main container with padding
        main_container = tk.Frame(
            self.root,
            bg=UI_COLORS["app_background"]
        )
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Board
        left_frame = tk.Frame(
            main_container,
            bg=UI_COLORS["app_background"]
        )
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Board title
        board_title = tk.Label(
            left_frame,
            text="MONOPOLY BOARD",
            font=FONTS["title_large"],
            bg=UI_COLORS["app_background"],
            fg=BOARD_COLORS["go_background"]
        )
        board_title.pack(pady=(0, 10))
        
        # Board canvas
        self.board = AuthenticMonopolyBoard(
            left_frame,
            self.game_controller.board,
            on_property_click=self._on_property_click
        )
        
        # Right side - Panels
        right_frame = tk.Frame(
            main_container,
            bg=UI_COLORS["app_background"],
            width=SIZES["side_panel_width"]
        )
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Scrollable container for panels
        canvas = tk.Canvas(
            right_frame,
            bg=UI_COLORS["app_background"],
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=UI_COLORS["app_background"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Player panel
        self.player_panel = MonopolyPlayerPanel(
            scrollable_frame,
            [self.game_controller.get_player_info(p.name) 
             for p in self.game_controller.players]
        )
        self.player_panel.get_frame().pack(fill="x", pady=(0, 10))
        
        # Control panel
        control_callbacks = {
            "on_roll_dice": self._on_roll_dice,
            "on_buy_property": self._on_buy_property,
            "on_skip_purchase": self._on_skip_purchase
        }
        self.control_panel = MonopolyControlPanel(scrollable_frame, control_callbacks)
        self.control_panel.get_frame().pack(fill="x", pady=(0, 10))
        
        # Property card
        self.property_card = MonopolyPropertyCard(scrollable_frame)
        self.property_card.get_frame().pack(fill="x", pady=(0, 10))
        
        # Game log
        self.game_log = MonopolyGameLog(scrollable_frame)
        self.game_log.get_frame().pack(fill="x", expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _setup_game_callbacks(self):
        """Setup callbacks between game controller and GUI"""
        self.game_controller.set_callbacks(
            on_player_moved=self._on_player_moved,
            on_balance_changed=self._on_balance_changed,
            on_property_purchased=self._on_property_purchased,
            on_game_event=self._on_game_event,
            on_turn_changed=self._on_turn_changed,
            on_dice_rolled=self._on_dice_rolled
        )
    
    def _show_welcome_screen(self):
        """Show welcome screen with game options"""
        welcome = tk.Toplevel(self.root)
        welcome.title("Welcome to Monopoly!")
        welcome.geometry("500x400")
        welcome.configure(bg=UI_COLORS["panel_background"])
        welcome.transient(self.root)
        
        # Center the welcome window
        welcome.update_idletasks()
        x = (welcome.winfo_screenwidth() - 500) // 2
        y = (welcome.winfo_screenheight() - 400) // 2
        welcome.geometry(f"+{x}+{y}")
        
        # Title
        title = tk.Label(
            welcome,
            text="MONOPOLY",
            font=("Times New Roman", 36, "bold"),
            bg=UI_COLORS["panel_background"],
            fg=BOARD_COLORS["go_background"]
        )
        title.pack(pady=30)
        
        subtitle = tk.Label(
            welcome,
            text="Property Trading Game",
            font=FONTS["title_medium"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_secondary"]
        )
        subtitle.pack()
        
        # Game options
        options_frame = tk.Frame(welcome, bg=UI_COLORS["panel_background"])
        options_frame.pack(pady=40)
        
        # Number of players
        tk.Label(
            options_frame,
            text="Number of Players:",
            font=FONTS["player_info"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.num_players = tk.IntVar(value=2)
        player_spinbox = tk.Spinbox(
            options_frame,
            from_=2, to=8,
            textvariable=self.num_players,
            width=5,
            font=FONTS["player_info"]
        )
        player_spinbox.grid(row=0, column=1, padx=10, pady=10)
        
        # AI players
        tk.Label(
            options_frame,
            text="AI Players:",
            font=FONTS["player_info"],
            bg=UI_COLORS["panel_background"],
            fg=UI_COLORS["text_primary"]
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.ai_players = tk.IntVar(value=1)
        ai_spinbox = tk.Spinbox(
            options_frame,
            from_=0, to=7,
            textvariable=self.ai_players,
            width=5,
            font=FONTS["player_info"]
        )
        ai_spinbox.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(welcome, bg=UI_COLORS["panel_background"])
        button_frame.pack(pady=30)
        
        start_btn = tk.Button(
            button_frame,
            text="Start Game",
            font=FONTS["button_text"],
            bg=UI_COLORS["button_primary"],
            fg="white",
            padx=20,
            pady=10,
            command=lambda: [welcome.destroy(), self._start_new_game()]
        )
        start_btn.pack(side="left", padx=10)
        
        quick_btn = tk.Button(
            button_frame,
            text="Quick Start",
            font=FONTS["button_text"],
            bg=UI_COLORS["button_secondary"],
            fg="white",
            padx=20,
            pady=10,
            command=lambda: [welcome.destroy(), self._quick_start()]
        )
        quick_btn.pack(side="left", padx=10)
    
    def _start_new_game(self):
        """Start a new game"""
        self.game_state["started"] = True
        self.game_controller.start_game()
        
        # Add players to board
        for i, player in enumerate(self.game_controller.players):
            self.board.add_player_token(player.name, i)
        
        # Set first player
        current_player = self.game_controller.get_current_player()
        self.player_panel.set_current_player(current_player.name)
        self.board.highlight_current_player(current_player.name)
        
        # Update UI
        self.control_panel.enable_roll(True)
        self.control_panel.update_turn_info(f"{current_player.name}'s turn - Roll the dice!")
        
        # Log game start
        self.game_log.add_event(f"New game started with {len(self.game_controller.players)} players", "success")
        self.game_log.add_event(f"{current_player.name} goes first", "info")
    
    def _quick_start(self):
        """Quick start with default settings"""
        self.num_players = tk.IntVar(value=4)
        self.ai_players = tk.IntVar(value=2)
        self._start_new_game()
    
    def _reset_game(self):
        """Reset the current game"""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.game_controller.__init__()
            self._setup_game_callbacks()
            self.game_state = {
                "started": False,
                "current_player": None,
                "turn_phase": "waiting",
                "dice_rolled": False
            }
            self.game_log.clear_log()
            self.game_log.add_event("Game reset", "info")
    
    def _on_roll_dice(self):
        """Handle dice roll"""
        if not self.game_controller.can_roll_dice():
            return {"success": False}
        
        # Animate dice
        self.control_panel.animate_dice_roll()
        self.control_panel.enable_roll(False)
        
        # Roll dice in controller
        result = self.game_controller.roll_dice()
        
        if result["success"]:
            # Show dice result
            self.root.after(1500, lambda: self._show_dice_result(result))
        
        return result
    
    def _show_dice_result(self, result):
        """Show dice result after animation"""
        die1, die2 = result["dice"]
        total = result["total"]
        
        self.control_panel.show_dice_result(die1, die2)
        
        current_player = self.game_controller.get_current_player()
        self.game_log.add_event(
            f"{current_player.name} rolled {die1} + {die2} = {total}",
            "info"
        )
        
        # Move player token
        old_pos = current_player.current_pos
        new_pos = result["new_position"]
        
        self.board.move_player_token(current_player.name, new_pos, animate=True)
        
        # Check if passed GO
        if new_pos < old_pos and new_pos != 0:
            self.game_log.add_event(f"{current_player.name} passed GO and collected $200!", "success")
        
        # Handle landing
        self.root.after(
            len(range(old_pos, new_pos if new_pos > old_pos else new_pos + 40)) * ANIMATION["token_move_speed"],
            lambda: self._handle_landing(result)
        )
    
    def _handle_landing(self, dice_result):
        """Handle player landing on a space"""
        current_player = self.game_controller.get_current_player()
        position = dice_result["new_position"]
        property_data = self.board.board_data[position] if position < len(self.board.board_data) else None
        
        if property_data:
            property_name = getattr(property_data, 'name', 'Unknown')
            self.game_log.add_event(f"{current_player.name} landed on {property_name}", "info")
            
            # Show property card
            self._show_property_info(position)
            
            # Check if can buy
            if self.game_controller.can_buy_property():
                self.control_panel.enable_purchase_buttons(True)
                self.control_panel.update_turn_info("Property available for purchase!")
                self.game_log.add_event(f"{property_name} is available for purchase", "warning")
            else:
                # End turn
                self.control_panel.enable_roll(True)
                self._next_turn()
    
    def _on_buy_property(self):
        """Handle property purchase"""
        result = self.game_controller.buy_property()
        
        if result.get("success"):
            current_player = self.game_controller.get_current_player()
            property_name = result.get("property_name", "Property")
            cost = result.get("cost", 0)
            
            self.game_log.add_event(
                f"{current_player.name} bought {property_name} for ${cost}",
                "success"
            )
            
            # Update player panel
            self.player_panel.update_player(
                current_player.name,
                self.game_controller.get_player_info(current_player.name)
            )
            
            # Update board
            position = current_player.current_pos
            self.board.show_property_ownership(position, current_player.name)
            
            # Disable purchase buttons
            self.control_panel.enable_purchase_buttons(False)
            
            # Next turn
            self._next_turn()
        
        return result
    
    def _on_skip_purchase(self):
        """Handle skipping property purchase"""
        current_player = self.game_controller.get_current_player()
        self.game_log.add_event(f"{current_player.name} declined to purchase", "info")
        
        self.control_panel.enable_purchase_buttons(False)
        self._next_turn()
        
        return {"success": True}
    
    def _next_turn(self):
        """Move to next player's turn"""
        self.game_controller.end_turn()
        
        # Update current player
        current_player = self.game_controller.get_current_player()
        self.player_panel.set_current_player(current_player.name)
        self.board.highlight_current_player(current_player.name)
        
        # Enable roll button
        self.control_panel.enable_roll(True)
        self.control_panel.update_turn_info(f"{current_player.name}'s turn - Roll the dice!")
        
        self.game_log.add_event(f"--- {current_player.name}'s turn ---", "info")
    
    def _on_property_click(self, position: int):
        """Handle property click on board"""
        self._show_property_info(position)
    
    def _show_property_info(self, position: int):
        """Show property information in card"""
        if position < len(self.board.board_data):
            property_data = self.board.board_data[position]
            
            # Create display data
            display_data = {
                "name": getattr(property_data, 'name', 'Unknown'),
                "color_group": getattr(property_data, 'color_group', ''),
                "cost": getattr(property_data, 'card_cost', 'N/A'),
                "owner": getattr(property_data, 'owner', 'Bank')
            }
            
            # Add rent information if available
            if hasattr(property_data, 'rent'):
                display_data["rent"] = property_data.rent
            
            self.property_card.show_property(display_data)
    
    def _on_player_moved(self, player_name: str, new_position: int):
        """Callback when player moves"""
        pass  # Handled in dice roll
    
    def _on_balance_changed(self, player_name: str, new_balance: int):
        """Callback when player balance changes"""
        self.player_panel.update_player(
            player_name,
            {"balance": new_balance}
        )
    
    def _on_property_purchased(self, player_name: str, property_name: str):
        """Callback when property is purchased"""
        pass  # Handled in buy property
    
    def _on_game_event(self, message: str, event_type: str = "info"):
        """Callback for game events"""
        self.game_log.add_event(message, event_type)
    
    def _on_turn_changed(self, player_name: str):
        """Callback when turn changes"""
        pass  # Handled in next turn
    
    def _on_dice_rolled(self, die1: int, die2: int):
        """Callback when dice are rolled"""
        pass  # Handled in roll dice
    
    def _show_settings(self):
        """Show game settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        
        # Add settings options
        tk.Label(
            settings_window,
            text="Game Settings",
            font=FONTS["title_medium"]
        ).pack(pady=20)
        
        tk.Label(
            settings_window,
            text="Settings coming soon...",
            font=FONTS["player_info"]
        ).pack(pady=50)
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
        HOW TO PLAY MONOPOLY:
        
        1. Roll the dice to move around the board
        2. Buy properties when you land on them
        3. Collect rent from other players
        4. Build houses and hotels
        5. Bankrupt all other players to win!
        
        CONTROLS:
        - Click 'Roll Dice' to take your turn
        - Click properties on the board for details
        - Use action buttons to buy or skip properties
        """
        
        messagebox.showinfo("How to Play", help_text)
    
    def _show_rules(self):
        """Show Monopoly rules"""
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Monopoly Rules")
        rules_window.geometry("600x400")
        rules_window.transient(self.root)
        
        # Add scrollable text with rules
        text_widget = tk.Text(
            rules_window,
            wrap="word",
            font=FONTS["player_info"],
            padx=10,
            pady=10
        )
        text_widget.pack(fill="both", expand=True)
        
        rules = """
        MONOPOLY RULES
        
        OBJECTIVE:
        Become the wealthiest player through buying, renting and selling property.
        
        GAMEPLAY:
        • Each player starts with $1,500
        • Players take turns rolling dice and moving around the board
        • When landing on unowned property, you may buy it
        • When landing on owned property, you must pay rent
        • Collect $200 when passing GO
        
        PROPERTIES:
        • Complete color groups to build houses and hotels
        • Houses cost varies by property
        • Maximum 4 houses per property, then upgrade to hotel
        
        SPECIAL SPACES:
        • GO: Collect $200 when passing
        • Jail: Various ways to get out
        • Free Parking: No action required
        • Taxes: Pay the required amount
        
        WINNING:
        The last player remaining after all others have gone bankrupt wins!
        """
        
        text_widget.insert("1.0", rules)
        text_widget.config(state="disabled")
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """
        MONOPOLY
        Property Trading Game
        
        Version: 1.0.0
        Author: Aleph Aseffa
        
        A faithful digital recreation of the classic
        Monopoly board game with authentic graphics
        and smooth gameplay.
        
        © 2024 - All Rights Reserved
        """
        
        messagebox.showinfo("About Monopoly", about_text)
    
    def _on_closing(self):
        """Handle window closing"""
        if self.game_state["started"]:
            if messagebox.askyesno("Quit Game", "Are you sure you want to quit the current game?"):
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


# Main entry point
if __name__ == "__main__":
    app = PolishedMonopolyGUI()
    app.run()