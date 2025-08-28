"""
@author: Aleph Aseffa
Unit Tests for Monopoly UI Components

Comprehensive unit tests for the polished Monopoly UI components,
ensuring code quality and reliability.
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.colors import *
from gui.authentic_board import AuthenticMonopolyBoard
from gui.polished_panels import (
    MonopolyPlayerPanel,
    MonopolyControlPanel,
    MonopolyPropertyCard,
    MonopolyGameLog
)


class TestColorFunctions(unittest.TestCase):
    """Test color utility functions"""
    
    def test_get_property_color(self):
        """Test property color retrieval"""
        self.assertEqual(get_property_color("Brown"), "#955436")
        self.assertEqual(get_property_color("Blue"), "#0072BB")
        self.assertEqual(get_property_color("Railroad"), "#000000")
        self.assertEqual(get_property_color("InvalidGroup"), "#FFFFFF")
    
    def test_get_player_color(self):
        """Test player color assignment"""
        # Test first 8 players get unique colors
        colors = [get_player_color(i) for i in range(8)]
        self.assertEqual(len(colors), len(set(colors)))  # All unique
        
        # Test wraparound for 9th player
        self.assertEqual(get_player_color(8), get_player_color(0))
    
    def test_darken_color(self):
        """Test color darkening"""
        darkened = darken_color("#FFFFFF", 0.5)
        self.assertEqual(darkened, "#7f7f7f")
        
        darkened = darken_color("#FF0000", 0.7)
        self.assertEqual(darkened, "#b20000")
    
    def test_lighten_color(self):
        """Test color lightening"""
        lightened = lighten_color("#000000", 0.5)
        self.assertEqual(lightened, "#7f7f7f")
        
        lightened = lighten_color("#FF0000", 0.3)
        self.assertEqual(lightened, "#ff4c4c")
    
    def test_create_gradient(self):
        """Test gradient creation"""
        gradient = create_gradient("#000000", "#FFFFFF", 5)
        self.assertEqual(len(gradient), 5)
        self.assertEqual(gradient[0], "#000000")
        self.assertEqual(gradient[-1], "#ffffff")
    
    def test_get_player_token_style(self):
        """Test player token style generation"""
        style = get_player_token_style(0)
        self.assertIn("fill", style)
        self.assertIn("outline", style)
        self.assertIn("width", style)
        self.assertIn("active_glow", style)
        self.assertEqual(style["width"], SIZES["token_border"])


class TestAuthenticMonopolyBoard(unittest.TestCase):
    """Test the authentic Monopoly board"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.board_data = [Mock(name=f"Property{i}", 
                              color_group="Brown",
                              card_cost=100) for i in range(40)]
        self.board = AuthenticMonopolyBoard(self.root, self.board_data)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_board_initialization(self):
        """Test board is properly initialized"""
        self.assertIsNotNone(self.board.canvas)
        self.assertEqual(self.board.board_size, SIZES["board_size"])
        self.assertEqual(len(self.board.property_rects), 40)
    
    def test_space_coordinates(self):
        """Test space coordinate calculation"""
        # Test GO corner (position 0)
        x, y, w, h, side = self.board._get_space_coords(0)
        self.assertEqual(side, "corner")
        self.assertEqual(w, SIZES["corner_size"])
        
        # Test bottom property (position 5)
        x, y, w, h, side = self.board._get_space_coords(5)
        self.assertEqual(side, "bottom")
        self.assertEqual(w, SIZES["property_width"])
        
        # Test left property (position 15)
        x, y, w, h, side = self.board._get_space_coords(15)
        self.assertEqual(side, "left")
        
        # Test top property (position 25)
        x, y, w, h, side = self.board._get_space_coords(25)
        self.assertEqual(side, "top")
        
        # Test right property (position 35)
        x, y, w, h, side = self.board._get_space_coords(35)
        self.assertEqual(side, "right")
    
    def test_add_player_token(self):
        """Test adding player tokens"""
        self.board.add_player_token("Player1", 0)
        self.assertIn("Player1", self.board.player_tokens)
        self.assertEqual(self.board.player_positions["Player1"], 0)
        
        self.board.add_player_token("Player2", 1)
        self.assertIn("Player2", self.board.player_tokens)
        self.assertEqual(len(self.board.player_tokens), 2)
    
    def test_move_player_token_no_animation(self):
        """Test moving player token without animation"""
        self.board.add_player_token("Player1", 0)
        self.board.move_player_token("Player1", 10, animate=False)
        self.assertEqual(self.board.player_positions["Player1"], 10)
    
    def test_token_offset_calculation(self):
        """Test token offset for multiple players"""
        offset1 = self.board._get_token_offset(0)
        offset2 = self.board._get_token_offset(1)
        offset3 = self.board._get_token_offset(2)
        
        # Offsets should be different for different players
        self.assertNotEqual(offset1, offset2)
        self.assertNotEqual(offset2, offset3)
    
    def test_property_selection(self):
        """Test property selection"""
        self.board._select_property(5)
        self.assertEqual(self.board.selected_property, 5)
        
        # Select another property
        self.board._select_property(10)
        self.assertEqual(self.board.selected_property, 10)
    
    def test_property_highlighting(self):
        """Test property highlighting"""
        self.board._highlight_property(5)
        self.assertEqual(self.board.highlighted_property, 5)
        
        self.board._clear_highlight()
        self.assertIsNone(self.board.highlighted_property)
    
    def test_split_name(self):
        """Test name splitting for display"""
        # Short name
        result = self.board._split_name("SHORT")
        self.assertEqual(result, ["SHORT"])
        
        # Long single word
        result = self.board._split_name("VERYLONGPROPERTYNAME", max_len=10)
        self.assertEqual(len(result[0]), 10)
        
        # Multiple words
        result = self.board._split_name("NEW YORK AVENUE", max_len=10)
        self.assertTrue(all(len(line) <= 10 for line in result))


class TestMonopolyPlayerPanel(unittest.TestCase):
    """Test the player information panel"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.players_data = [
            {"name": "Player1", "balance": 1500, "properties": 0},
            {"name": "Player2", "balance": 1500, "properties": 0}
        ]
        self.panel = MonopolyPlayerPanel(self.root, self.players_data)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_panel_initialization(self):
        """Test panel is properly initialized"""
        self.assertIsNotNone(self.panel.frame)
        self.assertEqual(len(self.panel.player_cards), 2)
        self.assertIn("Player1", self.panel.player_cards)
        self.assertIn("Player2", self.panel.player_cards)
    
    def test_update_player_balance(self):
        """Test updating player balance"""
        self.panel.update_player("Player1", {"balance": 2000, "properties": 3})
        
        widgets = self.panel.player_cards["Player1"]
        balance_text = widgets["balance_label"].cget("text")
        self.assertIn("2,000", balance_text)
        
        properties_text = widgets["properties_label"].cget("text")
        self.assertIn("3", properties_text)
    
    def test_set_current_player(self):
        """Test highlighting current player"""
        self.panel.set_current_player("Player1")
        
        # Check Player1 is highlighted
        p1_widgets = self.panel.player_cards["Player1"]
        self.assertEqual(p1_widgets["card"].cget("relief"), "raised")
        self.assertEqual(p1_widgets["card"].cget("bd"), 3)
        
        # Check Player2 is not highlighted
        p2_widgets = self.panel.player_cards["Player2"]
        self.assertEqual(p2_widgets["card"].cget("relief"), "solid")
        self.assertEqual(p2_widgets["card"].cget("bd"), 1)
    
    def test_jail_status_display(self):
        """Test jail status badge"""
        self.panel.update_player("Player1", {"in_jail": True})
        
        widgets = self.panel.player_cards["Player1"]
        # Badge should be visible (packed)
        self.assertIsNotNone(widgets["jail_badge"].winfo_manager())
    
    def test_bankrupt_status_display(self):
        """Test bankrupt status badge"""
        self.panel.update_player("Player2", {"bankrupt": True})
        
        widgets = self.panel.player_cards["Player2"]
        # Badge should be visible
        self.assertIsNotNone(widgets["bankrupt_badge"].winfo_manager())


class TestMonopolyControlPanel(unittest.TestCase):
    """Test the game control panel"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.callbacks = {
            "on_roll_dice": Mock(),
            "on_buy_property": Mock(),
            "on_skip_purchase": Mock()
        }
        self.panel = MonopolyControlPanel(self.root, self.callbacks)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_panel_initialization(self):
        """Test panel is properly initialized"""
        self.assertIsNotNone(self.panel.frame)
        self.assertIsNotNone(self.panel.dice_canvas)
        self.assertIsNotNone(self.panel.roll_button)
        self.assertIsNotNone(self.panel.buy_button)
        self.assertIsNotNone(self.panel.skip_button)
    
    def test_dice_display(self):
        """Test dice display updates"""
        self.panel.show_dice_result(3, 4)
        result_text = self.panel.dice_result.cget("text")
        self.assertIn("7", result_text)
        
        # Test doubles
        self.panel.show_dice_result(5, 5)
        result_text = self.panel.dice_result.cget("text")
        self.assertIn("DOUBLES", result_text)
    
    def test_button_states(self):
        """Test button enable/disable"""
        # Test roll button
        self.panel.enable_roll(True)
        self.assertEqual(self.panel.roll_button.cget("state"), "normal")
        
        self.panel.enable_roll(False)
        self.assertEqual(self.panel.roll_button.cget("state"), "disabled")
        
        # Test purchase buttons
        self.panel.enable_purchase_buttons(True)
        self.assertEqual(self.panel.buy_button.cget("state"), "normal")
        self.assertEqual(self.panel.skip_button.cget("state"), "normal")
        
        self.panel.enable_purchase_buttons(False)
        self.assertEqual(self.panel.buy_button.cget("state"), "disabled")
        self.assertEqual(self.panel.skip_button.cget("state"), "disabled")
    
    def test_turn_info_update(self):
        """Test turn information updates"""
        test_text = "Player 1's turn - Roll the dice!"
        self.panel.update_turn_info(test_text)
        self.assertEqual(self.panel.turn_info.cget("text"), test_text)
    
    def test_roll_button_callback(self):
        """Test roll button triggers callback"""
        self.panel.roll_button.invoke()
        self.callbacks["on_roll_dice"].assert_called_once()
    
    def test_buy_button_callback(self):
        """Test buy button triggers callback"""
        self.panel.buy_button.config(state="normal")
        self.panel.buy_button.invoke()
        self.callbacks["on_buy_property"].assert_called_once()


class TestMonopolyPropertyCard(unittest.TestCase):
    """Test the property information card"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.card = MonopolyPropertyCard(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_card_initialization(self):
        """Test card is properly initialized"""
        self.assertIsNotNone(self.card.frame)
        self.assertIsNotNone(self.card.property_card)
    
    def test_show_property_data(self):
        """Test displaying property information"""
        property_data = {
            "name": "Park Place",
            "color_group": "Blue",
            "cost": 350,
            "owner": "Player1",
            "rent": {
                0: 35,
                1: 175,
                2: 500,
                3: 1100,
                4: 1300,
                5: 1500
            }
        }
        
        self.card.show_property(property_data)
        
        # Check that property card has content
        children = self.card.property_card.winfo_children()
        self.assertGreater(len(children), 0)
    
    def test_show_no_property(self):
        """Test empty property state"""
        self.card.show_property(None)
        
        # Check for placeholder message
        children = self.card.property_card.winfo_children()
        self.assertEqual(len(children), 1)
        self.assertIsInstance(children[0], tk.Label)
    
    def test_colored_property_check(self):
        """Test colored property identification"""
        self.assertTrue(self.card._is_colored_property("Brown"))
        self.assertTrue(self.card._is_colored_property("Blue"))
        self.assertFalse(self.card._is_colored_property("Railroad"))
        self.assertFalse(self.card._is_colored_property("Utilities"))


class TestMonopolyGameLog(unittest.TestCase):
    """Test the game event log"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        self.log = MonopolyGameLog(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_log_initialization(self):
        """Test log is properly initialized"""
        self.assertIsNotNone(self.log.frame)
        self.assertIsNotNone(self.log.log_text)
        
        # Check welcome message
        content = self.log.log_text.get("1.0", "end")
        self.assertIn("Welcome to Monopoly", content)
    
    def test_add_event(self):
        """Test adding events to log"""
        self.log.add_event("Test event", "info")
        content = self.log.log_text.get("1.0", "end")
        self.assertIn("Test event", content)
        
        # Test different event types
        self.log.add_event("Success event", "success")
        self.log.add_event("Warning event", "warning")
        self.log.add_event("Error event", "error")
        
        content = self.log.log_text.get("1.0", "end")
        self.assertIn("Success event", content)
        self.assertIn("Warning event", content)
        self.assertIn("Error event", content)
    
    def test_clear_log(self):
        """Test clearing the log"""
        # Add some events
        self.log.add_event("Event 1", "info")
        self.log.add_event("Event 2", "info")
        
        # Clear log
        self.log.clear_log()
        
        content = self.log.log_text.get("1.0", "end")
        self.assertNotIn("Event 1", content)
        self.assertNotIn("Event 2", content)
        self.assertIn("Log cleared", content)
    
    def test_timestamp_format(self):
        """Test that timestamps are added"""
        self.log.add_event("Timestamped event", "info")
        content = self.log.log_text.get("1.0", "end")
        
        # Check for timestamp format [HH:MM:SS]
        import re
        timestamp_pattern = r'\[\d{2}:\d{2}:\d{2}\]'
        self.assertTrue(re.search(timestamp_pattern, content))


class TestIntegration(unittest.TestCase):
    """Integration tests for UI components working together"""
    
    def setUp(self):
        """Setup test environment"""
        self.root = tk.Tk()
        
        # Create all components
        self.board_data = [Mock(name=f"Property{i}") for i in range(40)]
        self.board = AuthenticMonopolyBoard(self.root, self.board_data)
        
        self.players_data = [
            {"name": "Player1", "balance": 1500, "properties": 0},
            {"name": "Player2", "balance": 1500, "properties": 0}
        ]
        self.player_panel = MonopolyPlayerPanel(self.root, self.players_data)
        
        self.callbacks = {
            "on_roll_dice": Mock(),
            "on_buy_property": Mock(),
            "on_skip_purchase": Mock()
        }
        self.control_panel = MonopolyControlPanel(self.root, self.callbacks)
        
        self.property_card = MonopolyPropertyCard(self.root)
        self.game_log = MonopolyGameLog(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_components_creation(self):
        """Test all components are created successfully"""
        self.assertIsNotNone(self.board.canvas)
        self.assertIsNotNone(self.player_panel.frame)
        self.assertIsNotNone(self.control_panel.frame)
        self.assertIsNotNone(self.property_card.frame)
        self.assertIsNotNone(self.game_log.frame)
    
    def test_game_flow_simulation(self):
        """Test simulated game flow"""
        # Add players to board
        self.board.add_player_token("Player1", 0)
        self.board.add_player_token("Player2", 1)
        
        # Set current player
        self.player_panel.set_current_player("Player1")
        self.board.highlight_current_player("Player1")
        
        # Simulate dice roll
        self.control_panel.show_dice_result(3, 4)
        self.game_log.add_event("Player1 rolled 7", "info")
        
        # Move player
        self.board.move_player_token("Player1", 7, animate=False)
        
        # Update player info
        self.player_panel.update_player("Player1", 
                                       {"balance": 1400, "properties": 1})
        
        # Show property
        property_data = {
            "name": "Vermont Avenue",
            "color_group": "Light Blue",
            "cost": 100,
            "owner": "Player1"
        }
        self.property_card.show_property(property_data)
        
        # Log purchase
        self.game_log.add_event("Player1 bought Vermont Avenue for $100", "success")
        
        # Verify states
        self.assertEqual(self.board.player_positions["Player1"], 7)
        widgets = self.player_panel.player_cards["Player1"]
        self.assertIn("1,400", widgets["balance_label"].cget("text"))


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)