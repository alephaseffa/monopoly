"""
@author: Aleph Aseffa
Created for Monopoly game

Contains the Chance card system implementation including card definitions,
deck management, and effect execution.
"""

import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.player_definitions import Player
    from classes.card_definitions import Card


class EffectType(Enum):
    MOVE_TO_POSITION = "move_to_position"
    MOVE_RELATIVE = "move_relative"
    PAY_MONEY = "pay_money"
    RECEIVE_MONEY = "receive_money"
    GO_TO_JAIL = "go_to_jail"
    GET_OUT_OF_JAIL_FREE = "get_out_of_jail_free"
    PROPERTY_REPAIRS = "property_repairs"
    ADVANCE_TO_NEAREST_RAILROAD = "advance_to_nearest_railroad"
    ADVANCE_TO_NEAREST_UTILITY = "advance_to_nearest_utility"
    COLLECT_FROM_ALL_PLAYERS = "collect_from_all_players"
    PAY_TO_ALL_PLAYERS = "pay_to_all_players"
    STREET_REPAIRS = "street_repairs"
    ADVANCE_TO_GO = "advance_to_go"


@dataclass
class ChanceCard:
    title: str
    description: str
    effect_type: EffectType
    effect_params: Dict[str, Any] = field(default_factory=dict)
    is_keepable: bool = False

    def execute(self, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None) -> None:
        ChanceCardExecutor.execute(self, player, board, all_players, chance_deck, community_chest_deck)


class ChanceCardExecutor:
    @staticmethod
    def execute(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None) -> None:
        print(f"\n{player.name} drew a Chance card:")
        print(f'"{card.title}" - {card.description}')
        
        method_name = f"_handle_{card.effect_type.value}"
        handler = getattr(ChanceCardExecutor, method_name)
        handler(card, player, board, all_players, chance_deck, community_chest_deck)

    @staticmethod
    def _handle_move_to_position(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        target_pos = card.effect_params['position']
        
        # Check if passing GO
        if target_pos < player.current_pos or (target_pos == 0):
            print(f"{player.name} passes GO and collects $200!")
            player.add_balance(200)
        
        player.current_pos = target_pos
        print(f"{player.name} moves to {board[target_pos].card_name}")
        # Restore check_pos call to trigger space effects (no all_players to prevent recursion)
        player.check_pos(board, chance_deck, community_chest_deck, None)

    @staticmethod
    def _handle_move_relative(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        spaces = card.effect_params['spaces']
        old_pos = player.current_pos
        player.current_pos = (player.current_pos + spaces) % 40
        
        # Check if passing GO (only when moving forward)
        if spaces > 0 and player.current_pos < old_pos:
            print(f"{player.name} passes GO and collects $200!")
            player.add_balance(200)
        
        print(f"{player.name} moves to {board[player.current_pos].card_name}")
        # Restore check_pos call to trigger space effects (no all_players to prevent recursion)
        player.check_pos(board, chance_deck, community_chest_deck, None)

    @staticmethod
    def _handle_pay_money(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        amount = card.effect_params['amount']
        print(f"{player.name} pays ${amount}")
        player.reduce_balance(amount)

    @staticmethod
    def _handle_receive_money(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        amount = card.effect_params['amount']
        print(f"{player.name} receives ${amount}")
        player.add_balance(amount)

    @staticmethod
    def _handle_go_to_jail(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        print(f"{player.name} goes directly to jail!")
        player.send_to_jail()
        player.in_jail = True

    @staticmethod
    def _handle_get_out_of_jail_free(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        print(f"{player.name} receives a Get Out of Jail Free card!")
        player.get_out_of_jail_cards.append(card)

    @staticmethod
    def _handle_property_repairs(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        house_cost = card.effect_params['house_cost']
        hotel_cost = card.effect_params['hotel_cost']
        
        total_cost = 0
        houses = 0
        hotels = 0
        
        for owned_card in player.cards_owned:
            if hasattr(owned_card, 'houses_built') and owned_card.houses_built > 0:
                if owned_card.houses_built == 5:  # Hotel
                    hotels += 1
                    total_cost += hotel_cost
                else:  # Houses
                    houses += owned_card.houses_built
                    total_cost += owned_card.houses_built * house_cost
        
        if total_cost > 0:
            print(f"{player.name} pays ${total_cost} for repairs ({houses} houses @ ${house_cost}, {hotels} hotels @ ${hotel_cost})")
            player.reduce_balance(total_cost)
        else:
            print(f"{player.name} has no properties requiring repairs")

    @staticmethod
    def _handle_advance_to_nearest_railroad(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        railroad_positions = [5, 15, 25, 35]  # Reading, Pennsylvania, B&O, Short Line
        current_pos = player.current_pos
        
        # Find next railroad
        next_railroad = None
        for pos in railroad_positions:
            if pos > current_pos:
                next_railroad = pos
                break
        
        # If no railroad ahead, go to first one (Reading Railroad)
        if next_railroad is None:
            next_railroad = railroad_positions[0]
            print(f"{player.name} passes GO and collects $200!")
            player.add_balance(200)
        
        player.current_pos = next_railroad
        railroad_card = board[next_railroad]
        print(f"{player.name} advances to the nearest railroad: {railroad_card.card_name}")
        
        # Pay double rent if owned by another player
        if railroad_card.owner != 'Bank' and railroad_card.owner.name != player.name:
            print(f"Pay double rent to {railroad_card.owner.name}!")
            rent_amt = 50 * railroad_card.owner.railroads_owned  # Double the normal rent
            print(f"{player.name} is paying ${rent_amt} as double rental charge to {railroad_card.owner.name}")
            player.reduce_balance(rent_amt)
            railroad_card.owner.add_balance(rent_amt)
        elif railroad_card.owner == 'Bank':
            # Option to buy
            if player.name == "AI":
                if player.balance > railroad_card.card_cost:
                    railroad_card.purchase_card(player)
                    print(f"{player.name} has purchased {railroad_card.card_name}")
            else:
                user_action = input("Do you want to buy the railroad? (y/n) ")
                if user_action == 'y':
                    railroad_card.purchase_card(player)

    @staticmethod
    def _handle_advance_to_nearest_utility(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        utility_positions = [12, 28]  # Electric Company, Water Works
        current_pos = player.current_pos
        
        # Find next utility
        next_utility = None
        for pos in utility_positions:
            if pos > current_pos:
                next_utility = pos
                break
        
        # If no utility ahead, go to first one (Electric Company)
        if next_utility is None:
            next_utility = utility_positions[0]
            print(f"{player.name} passes GO and collects $200!")
            player.add_balance(200)
        
        player.current_pos = next_utility
        utility_card = board[next_utility]
        print(f"{player.name} advances to the nearest utility: {utility_card.card_name}")
        
        # Pay 10 times dice roll if owned by another player
        if utility_card.owner != 'Bank' and utility_card.owner.name != player.name:
            dice_roll = player.roll_dice()
            rent_amt = dice_roll * 10
            print(f"Pay 10 times dice roll (${rent_amt}) to {utility_card.owner.name}!")
            player.reduce_balance(rent_amt)
            utility_card.owner.add_balance(rent_amt)
        elif utility_card.owner == 'Bank':
            # Option to buy
            if player.name == "AI":
                if player.balance > utility_card.card_cost:
                    utility_card.purchase_card(player)
                    print(f"{player.name} has purchased {utility_card.card_name}")
            else:
                user_action = input("Do you want to buy the utility? (y/n) ")
                if user_action == 'y':
                    utility_card.purchase_card(player)

    @staticmethod
    def _handle_collect_from_all_players(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        amount = card.effect_params['amount']
        if all_players:
            total_collected = 0
            for other_player in all_players:
                if other_player != player and not other_player.bankruptcy_status:
                    other_player.reduce_balance(amount)
                    total_collected += amount
                    print(f"{other_player.name} pays ${amount} to {player.name}")
            player.add_balance(total_collected)
            print(f"{player.name} collects ${total_collected} total from all other players!")
        else:
            # Fallback if no player list provided
            print(f"{player.name} collects ${amount} (no other players available)")
            player.add_balance(amount)

    @staticmethod
    def _handle_pay_to_all_players(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        amount = card.effect_params['amount']
        if all_players:
            total_paid = 0
            for other_player in all_players:
                if other_player != player and not other_player.bankruptcy_status:
                    other_player.add_balance(amount)
                    total_paid += amount
                    print(f"{player.name} pays ${amount} to {other_player.name}")
            player.reduce_balance(total_paid)
            print(f"{player.name} pays ${total_paid} total to all other players!")
        else:
            # Fallback if no player list provided
            print(f"{player.name} pays ${amount} (no other players available)")
            player.reduce_balance(amount)

    @staticmethod
    def _handle_street_repairs(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        house_cost = card.effect_params['house_cost']
        hotel_cost = card.effect_params['hotel_cost']
        
        total_cost = 0
        houses = 0
        hotels = 0
        
        for owned_card in player.cards_owned:
            if hasattr(owned_card, 'houses_built') and owned_card.houses_built > 0:
                if owned_card.houses_built == 5:  # Hotel
                    hotels += 1
                    total_cost += hotel_cost
                else:  # Houses
                    houses += owned_card.houses_built
                    total_cost += owned_card.houses_built * house_cost
        
        if total_cost > 0:
            print(f"{player.name} pays ${total_cost} for street repairs ({houses} houses @ ${house_cost}, {hotels} hotels @ ${hotel_cost})")
            player.reduce_balance(total_cost)
        else:
            print(f"{player.name} has no properties requiring street repairs")

    @staticmethod
    def _handle_advance_to_go(card: ChanceCard, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None):
        print(f"{player.name} advances to GO and collects $200!")
        player.current_pos = 0
        player.add_balance(200)


class ChanceDeck:
    def __init__(self, cards: List[ChanceCard]):
        self.cards = cards.copy()
        self.discard_pile = []
        random.shuffle(self.cards)

    def draw(self) -> ChanceCard:
        if not self.cards:
            self._reshuffle()
        
        card = self.cards.pop()
        
        # Keep cards go to discard pile, Get Out of Jail Free cards stay with player
        if not card.is_keepable:
            self.discard_pile.append(card)
        
        return card

    def return_card(self, card: ChanceCard):
        """Return a Get Out of Jail Free card to the deck"""
        self.discard_pile.append(card)

    def _reshuffle(self):
        """Reshuffle discard pile back into deck"""
        self.cards = self.discard_pile.copy()
        self.discard_pile = []
        random.shuffle(self.cards)
        print("Chance deck has been reshuffled!")


class CommunityChestDeck:
    def __init__(self, cards: List['CommunityChestCard']):
        self.cards = cards.copy()
        self.discard_pile = []
        random.shuffle(self.cards)

    def draw(self) -> 'CommunityChestCard':
        if not self.cards:
            self._reshuffle()
        
        card = self.cards.pop()
        
        # Keep cards go to discard pile, Get Out of Jail Free cards stay with player
        if not card.is_keepable:
            self.discard_pile.append(card)
        
        return card

    def return_card(self, card: 'CommunityChestCard'):
        """Return a Get Out of Jail Free card to the deck"""
        self.discard_pile.append(card)

    def _reshuffle(self):
        """Reshuffle discard pile back into deck"""
        self.cards = self.discard_pile.copy()
        self.discard_pile = []
        random.shuffle(self.cards)
        print("Community Chest deck has been reshuffled!")


# Standard Monopoly Chance Cards
CHANCE_CARDS = [
    ChanceCard(
        "Advance to GO",
        "Collect $200",
        EffectType.MOVE_TO_POSITION,
        {"position": 0}
    ),
    ChanceCard(
        "Advance to Illinois Avenue",
        "If you pass GO, collect $200",
        EffectType.MOVE_TO_POSITION,
        {"position": 24}
    ),
    ChanceCard(
        "Advance to St. Charles Place",
        "If you pass GO, collect $200",
        EffectType.MOVE_TO_POSITION,
        {"position": 11}
    ),
    ChanceCard(
        "Advance to nearest Railroad",
        "Pay owner twice the rental. If unowned, you may buy it",
        EffectType.ADVANCE_TO_NEAREST_RAILROAD
    ),
    ChanceCard(
        "Advance to nearest Railroad",
        "Pay owner twice the rental. If unowned, you may buy it",
        EffectType.ADVANCE_TO_NEAREST_RAILROAD
    ),
    ChanceCard(
        "Advance to nearest Utility",
        "If unowned you may buy it. If owned, pay 10 times dice roll",
        EffectType.ADVANCE_TO_NEAREST_UTILITY
    ),
    ChanceCard(
        "Bank pays you dividend",
        "Collect $50",
        EffectType.RECEIVE_MONEY,
        {"amount": 50}
    ),
    ChanceCard(
        "Get Out of Jail Free",
        "This card may be kept until needed or traded",
        EffectType.GET_OUT_OF_JAIL_FREE,
        is_keepable=True
    ),
    ChanceCard(
        "Go Back 3 Spaces",
        "",
        EffectType.MOVE_RELATIVE,
        {"spaces": -3}
    ),
    ChanceCard(
        "Go to Jail",
        "Go directly to Jail. Do not pass GO, do not collect $200",
        EffectType.GO_TO_JAIL
    ),
    ChanceCard(
        "Make general repairs",
        "Pay $25 per house, $100 per hotel",
        EffectType.PROPERTY_REPAIRS,
        {"house_cost": 25, "hotel_cost": 100}
    ),
    ChanceCard(
        "Pay poor tax",
        "Pay $15",
        EffectType.PAY_MONEY,
        {"amount": 15}
    ),
    ChanceCard(
        "Take a trip to Reading Railroad",
        "If you pass GO, collect $200",
        EffectType.MOVE_TO_POSITION,
        {"position": 5}
    ),
    ChanceCard(
        "Take a walk on the Boardwalk",
        "Advance to Boardwalk",
        EffectType.MOVE_TO_POSITION,
        {"position": 39}
    ),
    ChanceCard(
        "You have been elected Chairman",
        "Pay each player $50",
        EffectType.PAY_MONEY,
        {"amount": 50}  # TODO: This should pay to other players, not bank
    ),
    ChanceCard(
        "Your building loan matures",
        "Collect $150",
        EffectType.RECEIVE_MONEY,
        {"amount": 150}
    )
]


# Community Chest Card class (alias for ChanceCard for clarity)
@dataclass
class CommunityChestCard:
    title: str
    description: str
    effect_type: EffectType
    effect_params: Dict[str, Any] = field(default_factory=dict)
    is_keepable: bool = False

    def execute(self, player: 'Player', board: List['Card'], all_players: List['Player'] = None, chance_deck=None, community_chest_deck=None) -> None:
        ChanceCardExecutor.execute(self, player, board, all_players, chance_deck, community_chest_deck)


# Standard Monopoly Community Chest Cards
COMMUNITY_CHEST_CARDS = [
    CommunityChestCard(
        "Advance to GO",
        "Collect $200",
        EffectType.ADVANCE_TO_GO
    ),
    CommunityChestCard(
        "Bank error in your favor",
        "Collect $200",
        EffectType.RECEIVE_MONEY,
        {"amount": 200}
    ),
    CommunityChestCard(
        "Doctor's fees",
        "Pay $50",
        EffectType.PAY_MONEY,
        {"amount": 50}
    ),
    CommunityChestCard(
        "From sale of stock you get",
        "Collect $50",
        EffectType.RECEIVE_MONEY,
        {"amount": 50}
    ),
    CommunityChestCard(
        "Get Out of Jail Free",
        "This card may be kept until needed or traded",
        EffectType.GET_OUT_OF_JAIL_FREE,
        is_keepable=True
    ),
    CommunityChestCard(
        "Go to Jail",
        "Go directly to Jail. Do not pass GO, do not collect $200",
        EffectType.GO_TO_JAIL
    ),
    CommunityChestCard(
        "Holiday fund matures",
        "Receive $100",
        EffectType.RECEIVE_MONEY,
        {"amount": 100}
    ),
    CommunityChestCard(
        "Income tax refund",
        "Collect $20",
        EffectType.RECEIVE_MONEY,
        {"amount": 20}
    ),
    CommunityChestCard(
        "It is your birthday",
        "Collect $10 from every player",
        EffectType.COLLECT_FROM_ALL_PLAYERS,
        {"amount": 10}
    ),
    CommunityChestCard(
        "Life insurance matures",
        "Collect $100",
        EffectType.RECEIVE_MONEY,
        {"amount": 100}
    ),
    CommunityChestCard(
        "Pay hospital fees",
        "Pay $100",
        EffectType.PAY_MONEY,
        {"amount": 100}
    ),
    CommunityChestCard(
        "Pay school fees",
        "Pay $50",
        EffectType.PAY_MONEY,
        {"amount": 50}
    ),
    CommunityChestCard(
        "Receive consultancy fee",
        "Collect $25",
        EffectType.RECEIVE_MONEY,
        {"amount": 25}
    ),
    CommunityChestCard(
        "You are assessed for street repairs",
        "$40 per house, $115 per hotel",
        EffectType.STREET_REPAIRS,
        {"house_cost": 40, "hotel_cost": 115}
    ),
    CommunityChestCard(
        "You have won second prize in a beauty contest",
        "Collect $10",
        EffectType.RECEIVE_MONEY,
        {"amount": 10}
    ),
    CommunityChestCard(
        "You inherit",
        "Collect $100",
        EffectType.RECEIVE_MONEY,
        {"amount": 100}
    )
]