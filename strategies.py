from game_core_entities import Hand
from abc import ABC, abstractmethod
from enum import Enum

class Actions(Enum):
    HIT = 'HIT'
    DOUBLE = 'DOUBLE'
    SPLIT = 'SPLIT'
    STAY = 'STAY'

class BasicStrategy:

    @staticmethod
    def is_soft_hand(player_hand):
        return any(card.value == 'A' for card in player_hand.cards) and player_hand.compute_value() + 10 <= 21

    @staticmethod
    def is_pair(player_hand):
        return len(player_hand.cards) == 2 and player_hand.cards[0].value == player_hand.cards[1].value

    @staticmethod
    def optimal_move(player_hand: Hand, dealer_hand: Hand):
        dealer_value = dealer_hand.compute_value()
        hand_value = player_hand.compute_value()

        # Pair handling
        if BasicStrategy.is_pair(player_hand):
            pair_value = player_hand.cards[0].value
            if pair_value == 'A' or pair_value == '8':
                return 'SPLIT'
            elif pair_value == '9' and dealer_value not in [7, 10, 11]:
                return 'SPLIT'
            elif (pair_value == '7' or pair_value == '3'or pair_value == '2') and dealer_value < 8:
                return 'SPLIT'
            elif pair_value == '6' and dealer_value < 7:
                return 'SPLIT'
            elif pair_value == '4' and dealer_value in [5, 6]:
                return 'SPLIT'

        # Soft totals
        if BasicStrategy.is_soft_hand(player_hand):
            if hand_value == 18:
                return 'DOUBLE' if 2 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            if hand_value == 17:
                return 'DOUBLE' if 3 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            if hand_value == 16:
                return 'DOUBLE' if 4 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            if hand_value == 15:
                return 'DOUBLE' if 4 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            if hand_value == 14:
                return 'DOUBLE' if 5 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            if hand_value == 13:
                return 'DOUBLE' if 5 <= dealer_value <= 6 else 'HIT' if dealer_value in [9, 10, 11] else 'STAND'
            

        # Hard totals
        if hand_value >= 17:
            return 'STAND'
        elif hand_value <= 11:
            return 'HIT'
        elif hand_value == 12:
            return 'HIT' if dealer_value in [2, 3, 7, 8, 9, 10, 11] else 'STAND'
        else:
            return 'HIT' if dealer_value >= 7 else 'STAND'
        return 'HIT'  


class HiLoCardCountingStrategy:
    def __init__(self, base_bet=1):
        self.base_bet = base_bet
        self.running_count = 0
        self.true_count = 0
        self.decks_in_game = 3  #as per the Deck class initialization
        self.cards_seen = 0
        self.bet_increase_factor = max(1, self.true_count)

    def adjust_for_card(self, card):
        if card.value in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.value in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1
        self.cards_seen += 1
        self.update_true_count()

    def update_true_count(self):
        decks_remaining = max(self.decks_in_game - (self.cards_seen / 52), 1)
        self.true_count = self.running_count / decks_remaining

    def adjust_bet_based_on_count(self):
        if self.true_count <= 1:
            return self.base_bet
        else:
            return min(self.base_bet * self.bet_increase_factor, self.base_bet + self.true_count - 1)

    def optimal_move(self, player_hand, dealer_hand):
        # same as Basic strat for now
        return BasicStrategy.optimal_move(player_hand, dealer_hand)
    
    def reset_count(self):
        """
        Resets the running count, true count, and cards seen to start fresh when a new deck is shuffled into play.
        """
        self.running_count = 0
        self.true_count = 0
        self.cards_seen = 0