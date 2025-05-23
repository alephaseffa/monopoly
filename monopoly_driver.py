"""
@author: Aleph Aseffa
Date created: 7/14/2019



"""

from classes import player_definitions as p_def
from game import information as info
from game.initialization import get_player_info  # Import the new function
from ai import ai

board = info.initialize_cards_and_board()

# Get player information dynamically
player_list = get_player_info()

# Find the AI player, if one exists, and assign it to the Computer variable.
Computer = None
for player in player_list:
    if player.name == "AI":
        Computer = player
        break


def count_bankrupt_players(players):
    """
    Counts how many players have been bankrupted.
    :param players: list, players that are playing the game.
    :return: int, number of players that are bankrupt.
    """
    counter = 0
    for player in players:
        if player.bankruptcy_status:
            counter += 1
    return counter


def display_winner(players):
    """
    Prints out which player has won.
    :param players: list, players that are playing the game.
    :return: None.
    """
    for player in players:
        if player.bankruptcy_status == False:
            return player.name


if __name__ == "__main__":
    print("Beginning game!")
    info.display_instructions()

    i = 0
    # continue running while there is more than one non-bankrupt player remaining.
    while count_bankrupt_players(player_list) != len(player_list)-1:
        i = i % len(player_list)

        print()
        print(f"{player_list[i].name}'s turn:")

        # AI's turn
        if player_list[i].name == "AI":
            if Computer is not None: # Ensure Computer is the AI object
                ai.move(Computer, board)
                # Check for AI bankruptcy after AI move (if ai.move doesn't handle it)
                if Computer.is_bankrupt: # Assuming is_bankrupt is a boolean attribute
                    print("AI is bankrupt")
                    # Consider removing AI from player_list or marking as inactive
            else:
                # This case should ideally not be reached if player_list[i].name == "AI"
                # and Computer variable is correctly assigned.
                print("Error: AI player found in list but 'Computer' variable is None.")
        # Human player's turn
        else:
            user_choice = input("What do you want to do? ")
            # player_action will receive Computer, which might be None.
            # The player_action method itself needs to handle cases where Computer is None if it uses it.
            result = player_list[i].player_action(user_choice, player_list, Computer, board)
            while result == -1:  # keep asking the user until they choose to roll the dice.
                user_choice = input("What do you want to do? ")
                result = player_list[i].player_action(user_choice, player_list, Computer, board)
            new_pos = player_list[i].move_player(result)
            player_list[i].check_pos(board)
            # Check for human player bankruptcy after their action (if player_action doesn't handle it)
            # if player_list[i].is_bankrupt:
            # print(f"{player_list[i].name} is bankrupt")
            # Consider removing player from player_list or marking as inactive


        i += 1

    print(f"Game over! {display_winner(player_list)} has won!")
