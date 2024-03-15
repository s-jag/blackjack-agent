from game_simulator import Hand
from abc import ABC, abstractmethod
from enum import Enum

class Actions(Enum):
    HIT = 'HIT'
    DOUBLE = 'DOUBLE'
    SPLIT = 'SPLIT'
    STAY = 'STAY'


class Strategy(ABC):
    def __init__(self, player_hand: Hand, dealer_hand: Hand, description=''):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.description = description

    @abstractmethod
    def compute_optimal_move(self):
        pass