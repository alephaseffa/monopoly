import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.player_definitions import Player

class TestPlayerActions(unittest.TestCase):

    @patch('builtins.print')
    def test_trade_with_ai_no_ai_present(self, mock_print):
        # Create a human player instance
        # Player(name, balance, cards_owned, current_pos, in_jail, railroads_owned, doubles_counter, amount_owed, bankruptcy_status)
        # The arguments for Player.__init__ are:
        # name, balance, cards_owned, current_pos, in_jail, railroads_owned, doubles_counter, amount_owed, bankruptcy_status
        # For the test, many of these can be default values.
        human_player = Player(name="Human", balance=1500, cards_owned=[], current_pos=0, 
                              in_jail=False, railroads_owned=0, doubles_counter=0, 
                              amount_owed=0, bankruptcy_status=False)
        
        # Call trade_with_ai with computer=None
        # The 'board' argument is not deeply used in the path where computer is None,
        # so an empty list or a mock object would suffice.
        human_player.trade_with_ai(computer=None, board=[])
        
        # Assert that print was called with the specific message
        mock_print.assert_called_with("There is no AI player in the game to trade with.")

if __name__ == '__main__':
    unittest.main()
