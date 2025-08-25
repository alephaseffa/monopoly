"""
@author: Aleph Aseffa
Game Controller for Monopoly GUI

Bridges the GUI interface with existing game logic, handling events
and state synchronization between the visual interface and game engine.
"""

import tkinter as tk
from tkinter import messagebox
from typing import List, Callable, Optional, Dict, Any
import sys
import os

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import player_definitions as p_def
from game import information as info
from ai import ai

class GameController:
    def __init__(self):
        """Initialize the game controller with all necessary game components"""
        # Initialize game components
        self.board = info.initialize_cards_and_board()
        self.chance_deck = info.initialize_chance_deck()
        
        # Initialize players
        self.players = [
            p_def.Player("Player 1", 1500, [], 0, False, 0, 0, 0, False),
            p_def.Player("Player 2", 1500, [], 0, False, 0, 0, 0, False),
            p_def.Player("AI", 1500, [], 0, False, 0, 0, 0, False)
        ]
        
        # Game state
        self.current_player_index = 0
        self.game_started = False
        self.game_over = False
        self.turn_actions_completed = False
        
        # GUI callbacks
        self.on_player_moved = None  # Callback when player position changes
        self.on_balance_changed = None  # Callback when player balance changes
        self.on_property_purchased = None  # Callback when property is purchased
        self.on_game_event = None  # Callback for general game events
        self.on_turn_changed = None  # Callback when turn changes
        self.on_dice_rolled = None  # Callback when dice are rolled
        
        # Current turn state
        self.last_dice_roll = None
        self.turn_phase = "waiting_for_roll"  # waiting_for_roll, rolled, action_required, turn_complete
        
    def set_callbacks(self, **callbacks):
        """Set GUI callback functions"""
        for name, callback in callbacks.items():
            if hasattr(self, name):
                setattr(self, name, callback)
    
    def start_game(self):
        """Start a new game"""
        self.game_started = True
        self.game_over = False
        self.current_player_index = 0
        self.turn_phase = "waiting_for_roll"
        
        # Notify GUI of initial state
        self._notify_turn_changed()
        self._notify_game_event(f"Game started! {self.get_current_player().name}'s turn.")
        
    def get_current_player(self):
        """Get the current player object"""
        return self.players[self.current_player_index]
    
    def get_player_by_name(self, name: str):
        """Get player by name"""
        for player in self.players:
            if player.name == name:
                return player
        return None
    
    def can_roll_dice(self) -> bool:
        """Check if current player can roll dice"""
        return (self.game_started and not self.game_over and 
                self.turn_phase == "waiting_for_roll")
    
    def can_buy_property(self) -> bool:
        """Check if current player can buy current property"""
        if self.turn_phase != "action_required":
            return False
            
        current_player = self.get_current_player()
        current_property = self.board[current_player.current_pos]
        
        return (hasattr(current_property, 'card_cost') and 
                current_property.card_cost != "N/A" and
                current_property.owner == "Bank" and
                current_player.balance >= current_property.card_cost)
    
    def roll_dice(self) -> Dict[str, Any]:
        """
        Handle dice roll for current player
        :return: Dictionary with roll results and game state
        """
        if not self.can_roll_dice():
            return {"success": False, "message": "Cannot roll dice now"}
            
        current_player = self.get_current_player()
        
        # Handle jail logic
        if current_player.in_jail:
            return self._handle_jail_turn(current_player)
        
        # Regular dice roll
        dice_result = current_player.roll_dice()
        self.last_dice_roll = dice_result
        
        # Move player
        old_position = current_player.current_pos
        new_position = current_player.move_player(dice_result)
        new_position = new_position % 40  # Handle board wrapping
        
        # Notify GUI of movement
        if self.on_player_moved:
            self.on_player_moved(current_player.name, old_position, new_position)
        
        if self.on_dice_rolled:
            self.on_dice_rolled(dice_result, current_player.name)
        
        # Process landing on the new space
        result = self._process_space_landing(current_player)
        
        return {
            "success": True,
            "dice_roll": dice_result,
            "old_position": old_position,
            "new_position": new_position,
            "message": result.get("message", ""),
            "requires_action": result.get("requires_action", False)
        }
    
    def _handle_jail_turn(self, player) -> Dict[str, Any]:
        """Handle turn for player in jail"""
        # Check if player has Get Out of Jail Free card
        if player.get_out_of_jail_cards:
            response = messagebox.askyesno(
                "Get Out of Jail Free",
                f"{player.name} has a Get Out of Jail Free card. Use it?"
            )
            if response:
                card = player.get_out_of_jail_cards.pop()
                self.chance_deck.return_card(card)
                player.in_jail = False
                self._notify_game_event(f"{player.name} uses Get Out of Jail Free card!")
                
                # Roll dice and move
                dice_result = player.roll_dice()
                old_pos = player.current_pos
                new_pos = player.move_player(dice_result)
                
                if self.on_player_moved:
                    self.on_player_moved(player.name, old_pos, new_pos % 40)
                    
                result = self._process_space_landing(player)
                return {
                    "success": True,
                    "dice_roll": dice_result,
                    "message": "Used Get Out of Jail Free card!",
                    "requires_action": result.get("requires_action", False)
                }
        
        # Option to pay bail
        if player.balance >= 50:
            response = messagebox.askyesno(
                "Pay Bail",
                f"{player.name}, pay $50 bail to get out of jail?"
            )
            if response:
                player.reduce_balance(50)
                player.in_jail = False
                self._notify_balance_changed(player.name, player.balance)
                self._notify_game_event(f"{player.name} pays $50 bail!")
                
                # Roll dice and move
                dice_result = player.roll_dice()
                old_pos = player.current_pos
                new_pos = player.move_player(dice_result)
                
                if self.on_player_moved:
                    self.on_player_moved(player.name, old_pos, new_pos % 40)
                    
                result = self._process_space_landing(player)
                return {
                    "success": True,
                    "dice_roll": dice_result,
                    "message": "Paid bail and got out of jail!",
                    "requires_action": result.get("requires_action", False)
                }
        
        # Try to roll doubles
        dice_result = player.roll_dice()
        # TODO: Implement doubles detection
        self._notify_game_event(f"{player.name} failed to roll doubles. Still in jail.")
        self._end_turn()
        
        return {
            "success": True,
            "dice_roll": dice_result,
            "message": "Failed to roll doubles. Turn ends.",
            "requires_action": False
        }
    
    def _process_space_landing(self, player) -> Dict[str, Any]:
        """Process player landing on a space"""
        current_property = self.board[player.current_pos]
        
        # Use existing check_pos logic but capture the result
        if player.name == "AI":
            # For AI, check_pos returns 1 if property can be purchased
            purchasable = player.check_pos(self.board, self.chance_deck)
            if purchasable:
                self.turn_phase = "action_required"
                return {
                    "requires_action": True,
                    "message": f"AI can purchase {current_property.card_name}"
                }
        else:
            # For human players, check_pos handles the interaction
            # We need to modify this to work with GUI
            result = self._check_position_gui(player, current_property)
            return result
        
        # If no action required, end turn
        self._end_turn()
        return {"requires_action": False, "message": "Turn complete"}
    
    def _check_position_gui(self, player, property_card) -> Dict[str, Any]:
        """GUI version of check_pos logic"""
        if property_card.card_cost == "N/A":  # Non-purchasable space
            if property_card.card_name == 'Jail/Visiting Jail':
                self._notify_game_event(f"{player.name} is visiting jail.")
                
            elif property_card.card_name == 'Luxury Tax':
                self._notify_game_event(f"{player.name} pays $75 luxury tax")
                player.reduce_balance(75)
                self._notify_balance_changed(player.name, player.balance)
                
            elif property_card.card_name == 'Income Tax':
                self._notify_game_event(f"{player.name} pays $200 income tax")
                player.reduce_balance(200)
                self._notify_balance_changed(player.name, player.balance)
                
            elif property_card.card_name == 'Go to Jail':
                self._notify_game_event(f"{player.name} goes to jail!")
                player.send_to_jail()
                player.in_jail = True
                if self.on_player_moved:
                    self.on_player_moved(player.name, player.current_pos, 10)
                    
            elif property_card.card_name == 'Chance':
                self._notify_game_event(f"{player.name} drew a Chance card!")
                card = self.chance_deck.draw()
                card.execute(player, self.board)
                
            elif property_card.card_name == 'Community Chest':
                self._notify_game_event(f"{player.name} landed on Community Chest")
                messagebox.showinfo("Community Chest", "Community Chest cards not yet implemented")
                
            else:
                self._notify_game_event(f"{player.name} landed on {property_card.card_name}")
            
            self._end_turn()
            return {"requires_action": False}
            
        else:  # Purchasable property
            if property_card.mortgaged:
                self._notify_game_event(f"{player.name} landed on mortgaged property")
                self._end_turn()
                return {"requires_action": False}
                
            elif property_card.owner != 'Bank':
                if property_card.owner.name == player.name:
                    self._notify_game_event(f"{player.name} landed on their own property")
                else:
                    self._notify_game_event(f"{player.name} pays rent to {property_card.owner.name}")
                    player.charge_rent(property_card)
                    self._notify_balance_changed(player.name, player.balance)
                    self._notify_balance_changed(property_card.owner.name, property_card.owner.balance)
                self._end_turn()
                return {"requires_action": False}
                
            else:  # Property available for purchase
                self.turn_phase = "action_required"
                return {
                    "requires_action": True,
                    "message": f"{property_card.card_name} is available for ${property_card.card_cost}"
                }
    
    def buy_property(self) -> Dict[str, Any]:
        """Handle property purchase"""
        if not self.can_buy_property():
            return {"success": False, "message": "Cannot buy property now"}
            
        current_player = self.get_current_player()
        current_property = self.board[current_player.current_pos]
        
        # Execute purchase
        current_property.purchase_card(current_player)
        
        # Notify GUI
        self._notify_balance_changed(current_player.name, current_player.balance)
        self._notify_property_purchased(current_player.current_pos, current_player.name)
        self._notify_game_event(f"{current_player.name} bought {current_property.card_name} for ${current_property.card_cost}!")
        
        # End turn
        self._end_turn()
        
        return {
            "success": True,
            "message": f"Purchased {current_property.card_name}!"
        }
    
    def skip_purchase(self) -> Dict[str, Any]:
        """Skip purchasing current property"""
        if self.turn_phase != "action_required":
            return {"success": False, "message": "No action to skip"}
            
        current_player = self.get_current_player()
        current_property = self.board[current_player.current_pos]
        
        self._notify_game_event(f"{current_player.name} declined to buy {current_property.card_name}")
        self._end_turn()
        
        return {"success": True, "message": "Skipped purchase"}
    
    def _end_turn(self):
        """End current player's turn and advance to next player"""
        # Check for bankruptcy
        if self._check_bankruptcies():
            return  # Game might be over
        
        # Advance to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Skip bankrupt players
        while self.players[self.current_player_index].bankruptcy_status:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        self.turn_phase = "waiting_for_roll"
        self.last_dice_roll = None
        
        # Check for game over
        if self._count_active_players() <= 1:
            self._end_game()
            return
        
        # Handle AI turn
        if self.get_current_player().name == "AI":
            self._process_ai_turn()
        else:
            self._notify_turn_changed()
    
    def _process_ai_turn(self):
        """Process AI player turn automatically"""
        ai_player = self.get_current_player()
        
        if ai_player.in_jail:
            ai.leave_jail(ai_player, self.board, self.chance_deck)
        else:
            ai.move(ai_player, self.board, self.chance_deck)
        
        # Notify GUI of AI actions
        self._notify_balance_changed(ai_player.name, ai_player.balance)
        
        # End AI turn
        self._end_turn()
    
    def _check_bankruptcies(self) -> bool:
        """Check for player bankruptcies"""
        bankruptcies = 0
        for player in self.players:
            if player.bankruptcy_status:
                bankruptcies += 1
        
        return bankruptcies > 0
    
    def _count_active_players(self) -> int:
        """Count non-bankrupt players"""
        return sum(1 for player in self.players if not player.bankruptcy_status)
    
    def _end_game(self):
        """End the game and determine winner"""
        self.game_over = True
        winner = None
        
        for player in self.players:
            if not player.bankruptcy_status:
                winner = player
                break
        
        if winner:
            self._notify_game_event(f"Game Over! {winner.name} wins!")
            messagebox.showinfo("Game Over", f"{winner.name} has won the game!")
        else:
            self._notify_game_event("Game Over! No winner.")
    
    # Notification helpers
    def _notify_turn_changed(self):
        """Notify GUI that turn has changed"""
        if self.on_turn_changed:
            self.on_turn_changed(self.current_player_index, self.get_current_player().name)
    
    def _notify_balance_changed(self, player_name: str, new_balance: int):
        """Notify GUI of balance change"""
        if self.on_balance_changed:
            self.on_balance_changed(player_name, new_balance)
    
    def _notify_property_purchased(self, position: int, owner_name: str):
        """Notify GUI of property purchase"""
        if self.on_property_purchased:
            self.on_property_purchased(position, owner_name)
    
    def _notify_game_event(self, message: str):
        """Notify GUI of game event"""
        if self.on_game_event:
            self.on_game_event(message)
        print(f"[GAME] {message}")  # Also print to console for debugging
    
    # Getter methods for GUI
    def get_player_info(self, player_name: str) -> Dict[str, Any]:
        """Get comprehensive player information"""
        player = self.get_player_by_name(player_name)
        if not player:
            return {}
            
        return {
            "name": player.name,
            "balance": player.balance,
            "position": player.current_pos,
            "properties": len(player.cards_owned),
            "railroads": player.railroads_owned,
            "in_jail": player.in_jail,
            "bankrupt": player.bankruptcy_status,
            "jail_cards": len(player.get_out_of_jail_cards)
        }
    
    def get_property_info(self, position: int) -> Dict[str, Any]:
        """Get property information"""
        if position < 0 or position >= len(self.board):
            return {}
            
        property_card = self.board[position]
        
        return {
            "name": property_card.card_name,
            "color_group": getattr(property_card, 'color_group', 'N/A'),
            "cost": getattr(property_card, 'card_cost', 'N/A'),
            "rent": getattr(property_card, 'rent_prices', {}),
            "owner": property_card.owner.name if hasattr(property_card.owner, 'name') else str(property_card.owner),
            "mortgaged": getattr(property_card, 'mortgaged', False),
            "houses": getattr(property_card, 'houses_built', 0)
        }
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return {
            "started": self.game_started,
            "over": self.game_over,
            "current_player": self.current_player_index,
            "current_player_name": self.get_current_player().name if not self.game_over else None,
            "turn_phase": self.turn_phase,
            "last_dice_roll": self.last_dice_roll,
            "can_roll": self.can_roll_dice(),
            "can_buy": self.can_buy_property()
        }