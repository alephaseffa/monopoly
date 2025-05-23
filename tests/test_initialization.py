import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the Python path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.player_definitions import Player
from game.initialization import get_player_info

class TestGetPlayerInfo(unittest.TestCase):

    @patch('builtins.input', side_effect=["2", "Player1", "Player2", "no"])
    def test_get_player_info_humans_only(self, mock_input):
        players = get_player_info()
        self.assertEqual(len(players), 2)
        self.assertIsInstance(players[0], Player)
        self.assertEqual(players[0].name, "Player1")
        self.assertEqual(players[0].balance, 1500)
        self.assertIsInstance(players[1], Player)
        self.assertEqual(players[1].name, "Player2")
        self.assertEqual(players[1].balance, 1500)

    @patch('builtins.input', side_effect=["1", "Human1", "yes"])
    def test_get_player_info_with_ai(self, mock_input):
        players = get_player_info()
        self.assertEqual(len(players), 2)
        human_player_found = False
        ai_player_found = False
        for player in players:
            self.assertIsInstance(player, Player)
            self.assertEqual(player.balance, 1500)
            if player.name == "Human1":
                human_player_found = True
            elif player.name == "AI":
                ai_player_found = True
        self.assertTrue(human_player_found)
        self.assertTrue(ai_player_found)

    @patch('builtins.input', side_effect=["0", "abc", "1", "Solo", "no"])
    @patch('builtins.print') # Mock print to suppress output during test
    def test_get_player_info_invalid_num_players_then_valid(self, mock_print, mock_input):
        players = get_player_info()
        self.assertEqual(len(players), 1)
        self.assertIsInstance(players[0], Player)
        self.assertEqual(players[0].name, "Solo")
        self.assertEqual(players[0].balance, 1500)

    @patch('builtins.input', side_effect=["1", "Tester", "maybe", "yes"])
    @patch('builtins.print') # Mock print to suppress output during test
    def test_get_player_info_invalid_ai_choice_then_valid(self, mock_print, mock_input):
        players = get_player_info()
        self.assertEqual(len(players), 2)
        tester_player_found = False
        ai_player_found = False
        for player in players:
            self.assertIsInstance(player, Player)
            self.assertEqual(player.balance, 1500)
            if player.name == "Tester":
                tester_player_found = True
            elif player.name == "AI":
                ai_player_found = True
        self.assertTrue(tester_player_found)
        self.assertTrue(ai_player_found)

if __name__ == '__main__':
    unittest.main()
