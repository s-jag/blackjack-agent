from game_simulator import Hand
from abc import ABC, abstractmethod
from enum import Enum

class Actions(Enum):
    HIT = 'HIT'
    DOUBLE = 'DOUBLE'
    SPLIT = 'SPLIT'
    STAY = 'STAY'


class BasicStrategy:
    def __init__(self, player_hand: Hand, dealer_hand: Hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def is_soft_hand(self):
        return any(card.value == 'A' for card in self.player_hand.cards) and self.player_hand.compute_value() + 10 <= 21

    def is_pair(self):
        return len(self.player_hand.cards) == 2 and self.player_hand.cards[0].value == self.player_hand.cards[1].value

    def optimal_move(self):
        dealer_value = self.dealer_hand.compute_value()
        hand_value = self.player_hand.compute_value()

        # Pair handling
        if self.is_pair():
            pair_value = self.player_hand.cards[0].value
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
        if self.is_soft_hand():
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
