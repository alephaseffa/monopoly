"""
@author: Aleph Aseffa
Date created: 7/14/2019

Contains all the functions needed for the initialization of the game.


Functions that will be included:
- print header
- ask how many players will be playing
- for each one, take their username

"""
from classes.player_definitions import Player


def get_player_info():
    """
    Prompts for the number of human players and their names,
    and optionally adds an AI player.
    Creates Player objects and returns a list of them.
    """
    while True:
        try:
            num_human_players = int(input("How many human players will be playing? "))
            if num_human_players > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    players = []
    for i in range(1, num_human_players + 1):
        name = input(f"Enter name for Player {i}: ")
        players.append(Player(name=name, balance=1500, cards_owned=[], current_pos=0, in_jail=False, railroads_owned=0, doubles_counter=0, amount_owed=0, bankruptcy_status=False))

    while True:
        include_ai = input("Include AI player? (yes/no): ").lower()
        if include_ai in ['yes', 'no']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if include_ai == 'yes':
        players.append(Player(name="AI", balance=1500, cards_owned=[], current_pos=0, in_jail=False, railroads_owned=0, doubles_counter=0, amount_owed=0, bankruptcy_status=False))

    return players