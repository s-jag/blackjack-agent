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
