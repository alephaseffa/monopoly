"""
@author: Aleph Aseffa
Main Monopoly GUI Application

The primary GUI window that orchestrates all components including
the board, player panels, controls, and game logic integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import colors
from authentic_board import AuthenticMonopolyBoard
from game_controller import GameController
from ui_panels import PlayerInfoPanel, ActionControlPanel, PropertyDetailsPanel, GameLogPanel

class MonopolyGUI:
    """Main Monopoly GUI Application"""
    
    def __init__(self):
        """Initialize the main GUI application"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Monopoly Game")
        self.root.geometry(f"{colors.SIZES['window_width']}x{colors.SIZES['window_height']}")
        self.root.bg = colors.UI_COLORS["background"]
        self.root.resizable(True, True)
        
        # Initialize game controller
        self.game_controller = GameController()
        self._setup_controller_callbacks()
        
        # Create GUI components
        self._create_main_layout()
        self._create_menu_bar()
        
        # Initialize component data
        self._initialize_ui_components()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Center window on screen
        self._center_window()
        
    def _setup_controller_callbacks(self):
        """Setup callbacks between game controller and GUI"""
        self.game_controller.set_callbacks(
            on_player_moved=self._on_player_moved,
            on_balance_changed=self._on_balance_changed,
            on_property_purchased=self._on_property_purchased,
            on_game_event=self._on_game_event,
            on_turn_changed=self._on_turn_changed,
            on_dice_rolled=self._on_dice_rolled
        )
    
    def _create_main_layout(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg=colors.UI_COLORS["background"])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel (board)
        left_frame = tk.Frame(main_frame, bg=colors.UI_COLORS["background"])
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Board canvas
        self.board_canvas = AuthenticMonopolyBoard(
            left_frame, 
            self.game_controller.board,
            on_property_click=self._on_property_click
        )
        
        # Right panel (controls and info)
        right_frame = tk.Frame(main_frame, bg=colors.UI_COLORS["background"], width=colors.SIZES["panel_width"])
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)  # Maintain fixed width
        
        # Player info panel
        self.player_panel = PlayerInfoPanel(
            right_frame,
            [self.game_controller.get_player_info(p.name) for p in self.game_controller.players]
        )
        self.player_panel.get_frame().pack(fill="x", pady=(0, 10))
        
        # Action controls panel
        self.action_panel = ActionControlPanel(
            right_frame,
            on_roll_dice=self._on_roll_dice,
            on_buy_property=self._on_buy_property,
            on_skip_purchase=self._on_skip_purchase,
            on_end_turn=self._on_end_turn
        )
        self.action_panel.get_frame().pack(fill="x", pady=(0, 10))
        
        # Property details panel
        self.property_panel = PropertyDetailsPanel(right_frame)
        self.property_panel.get_frame().pack(fill="x", pady=(0, 10))
        
        # Game log panel
        self.log_panel = GameLogPanel(right_frame)
        self.log_panel.get_frame().pack(fill="both", expand=True)
        
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self._new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Save Game", command=self._save_game, state="disabled")
        game_menu.add_command(label="Load Game", command=self._load_game, state="disabled")
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self._on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self._zoom_in, state="disabled")
        view_menu.add_command(label="Zoom Out", command=self._zoom_out, state="disabled")
        view_menu.add_separator()
        view_menu.add_command(label="Center Board", command=self._center_board)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Play", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
        
    def _initialize_ui_components(self):
        """Initialize UI components with game data"""
        # Add player tokens to board
        for i, player in enumerate(self.game_controller.players):
            self.board_canvas.add_player_token(player.name, i)
        
        # Update initial property info (show GO space)
        go_property = self.game_controller.get_property_info(0)
        self.property_panel.update_property_info(go_property)
        
        # Show start game prompt
        self.log_panel.add_event("Click 'New Game' from the menu to start playing!", "system")
        
    # Game event handlers
    def _on_roll_dice(self) -> Dict[str, Any]:
        """Handle dice roll button click"""
        result = self.game_controller.roll_dice()
        
        if result.get("success", False):
            # Parse dice roll (assuming it returns total, we need to extract individual dice)
            total_roll = result["dice_roll"]
            die1 = total_roll // 2  # Simple approximation for display
            die2 = total_roll - die1
            
            self.action_panel.update_dice_display(die1, die2, total_roll)
            
            # Update turn info
            game_state = self.game_controller.get_game_state()
            self.action_panel.update_turn_info(
                game_state["current_player_name"],
                game_state["turn_phase"]
            )
        
        return result
        
    def _on_buy_property(self) -> Dict[str, Any]:
        """Handle buy property button click"""
        return self.game_controller.buy_property()
        
    def _on_skip_purchase(self) -> Dict[str, Any]:
        """Handle skip purchase button click"""
        return self.game_controller.skip_purchase()
        
    def _on_end_turn(self):
        """Handle end turn button click (if implemented)"""
        pass
        
    def _on_property_click(self, position: int):
        """Handle property click on board"""
        property_info = self.game_controller.get_property_info(position)
        self.property_panel.update_property_info(property_info)
        
        # Highlight clicked property
        # Remove previous highlights
        for i in range(40):
            self.board_canvas.highlight_property(i, False)
        
        # Highlight clicked property
        self.board_canvas.highlight_property(position, True)
        
        # Log property click
        property_name = property_info.get("name", "Unknown")
        self.log_panel.add_event(f"Viewing: {property_name}", "info")
        
    # Game controller callbacks
    def _on_player_moved(self, player_name: str, old_position: int, new_position: int):
        """Callback when player position changes"""
        self.board_canvas.move_player_token(player_name, new_position, animate=True)
        self.log_panel.add_event(f"{player_name} moved to position {new_position}", "info")
        
        # Update property display if it's current player's position
        current_player = self.game_controller.get_current_player()
        if player_name == current_player.name:
            property_info = self.game_controller.get_property_info(new_position)
            self.property_panel.update_property_info(property_info)
            
            # Highlight current position
            for i in range(40):
                self.board_canvas.highlight_property(i, False)
            self.board_canvas.highlight_property(new_position, True)
    
    def _on_balance_changed(self, player_name: str, new_balance: int):
        """Callback when player balance changes"""
        player_info = self.game_controller.get_player_info(player_name)
        self.player_panel.update_player_info(player_name, player_info)
        
        # Log significant balance changes
        self.log_panel.add_event(f"{player_name}'s balance: ${new_balance}", "info")
    
    def _on_property_purchased(self, position: int, owner_name: str):
        """Callback when property is purchased"""
        self.board_canvas.update_property_ownership(position, owner_name)
        
        property_info = self.game_controller.get_property_info(position)
        property_name = property_info.get("name", "Property")
        cost = property_info.get("cost", 0)
        
        self.log_panel.add_event(f"{owner_name} bought {property_name} for ${cost}!", "success")
    
    def _on_game_event(self, message: str):
        """Callback for general game events"""
        self.log_panel.add_event(message, "highlight")
    
    def _on_turn_changed(self, player_index: int, player_name: str):
        """Callback when turn changes to new player"""
        self.player_panel.set_current_player(player_name)
        
        # Update action panel
        game_state = self.game_controller.get_game_state()
        self.action_panel.update_turn_info(player_name, game_state["turn_phase"])
        self.action_panel.set_roll_enabled(game_state["can_roll"])
        
        # Log turn change
        self.log_panel.add_event(f"{player_name}'s turn begins!", "info")
    
    def _on_dice_rolled(self, dice_result: int, player_name: str):
        """Callback when dice are rolled"""
        # This is handled in _on_roll_dice, but we can add additional logic here
        pass
    
    # Menu handlers
    def _new_game(self):
        """Start a new game"""
        # Reset game state
        self.game_controller = GameController()
        self._setup_controller_callbacks()
        
        # Reset board
        for i, player in enumerate(self.game_controller.players):
            self.board_canvas.add_player(player.name, i, 0)
        
        # Reset UI panels
        for player in self.game_controller.players:
            player_info = self.game_controller.get_player_info(player.name)
            self.player_panel.update_player_info(player.name, player_info)
        
        # Clear property highlights
        for i in range(40):
            self.board_canvas.highlight_property(i, False)
            
        # Start the game
        self.game_controller.start_game()
        
        # Enable game controls
        self.action_panel.set_roll_enabled(True)
        
        self.log_panel.add_event("New game started! Player 1's turn.", "system")
    
    def _save_game(self):
        """Save current game (placeholder)"""
        messagebox.showinfo("Save Game", "Save game feature coming soon!")
    
    def _load_game(self):
        """Load saved game (placeholder)"""
        messagebox.showinfo("Load Game", "Load game feature coming soon!")
    
    def _zoom_in(self):
        """Zoom in on board (placeholder)"""
        messagebox.showinfo("Zoom", "Zoom feature coming soon!")
    
    def _zoom_out(self):
        """Zoom out on board (placeholder)"""
        messagebox.showinfo("Zoom", "Zoom feature coming soon!")
    
    def _center_board(self):
        """Center the board view"""
        # This could scroll the canvas to center if scrolling was implemented
        pass
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
MONOPOLY GAME HELP

HOW TO PLAY:
1. Click 'New Game' to start
2. Click 'Roll Dice' on your turn
3. Buy properties you land on or skip
4. Pay rent when landing on owned properties
5. Go to jail if you land on "Go to Jail"
6. Win by bankrupting all other players!

CONTROLS:
• Roll Dice: Roll to move around the board
• Buy Property: Purchase the property you landed on
• Skip Purchase: Decline to buy the property
• Click Properties: View property details

SPECIAL SPACES:
• GO: Collect $200 when passing
• Chance: Draw a chance card
• Community Chest: Draw community chest card
• Jail: Just visiting or imprisoned
• Free Parking: Nothing happens
• Go to Jail: Go directly to jail
• Taxes: Pay the specified amount

Good luck and have fun!
"""
        messagebox.showinfo("How to Play", help_text)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """
MONOPOLY GAME
Version 1.0

A classic board game implementation with GUI.

Created by: Aleph Aseffa
Built with: Python & Tkinter

Features:
• Full color game board
• Animated player tokens  
• Chance card system
• AI opponent
• Complete game mechanics

© 2024 - Educational Project
"""
        messagebox.showinfo("About Monopoly", about_text)
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        
        # Get window size
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point for GUI application"""
    try:
        app = MonopolyGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()