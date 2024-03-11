import random

SUITS = ['♠', '♥', '♦', '♣']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value
    
class Deck:
    def __init__(self, number_of_decks=3):
        one_deck = [Card(s, v) for s in SUITS for v in VALUES]
        self.cards = []
        for _ in range(number_of_decks):
            self.cards += one_deck
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self, cards=[]):
        self.cards = cards
        self.value = 0

    def add_to_hand(self, card: Card):
        self.cards.append(card)
        if self.compute_value() > 21:
            self.value = 0
            return True
        return False
    
    def compute_value(self):
        value_high = 0
        value_low = 0
        for card in self.cards:
            if card.value == 'A':
                value_high += 11
                value_low += 1
                continue
            value_high += max(1 + VALUES.indexof(card.value), 10)
            value_low += max(1 + VALUES.indexof(card.value), 10)
        self.value = value_high if value_high < 21 else value_low

class Player:
    def __init__(self, money=100, bet=1):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.money = money
        self.bet = bet
        self.playing = True if money > 0 else False
        self.double = False

    def play(self, dealer_hand: Hand, card: Card): # where the player logic comes in
        if self.hands[self.hand_idx].compute_value() + card.value <= 21:
            self.hit()
        else:
            self.stand()
    
    def reset(self):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.double = False

    def hit(self, card: Card):
        if not self.playing:
            return
        bust = self.hands[self.hand_idx].add_to_hand(card)
        if bust:
            self.money -= self.bet
            if self.money <= 0:
                self.playing = False
        if self.double:
            self.playing = False
    
    def stand(self):
        self.hand_idx += 1
        if self.hand_idx >= len(self.hands):
            self.hand_idx = 0
            self.playing = False

    def split(self, idx=-1):
        if not self.playing:
            return
        card = self.hands.pop(idx).cards[0]
        self.hands.extend([Hand([card]), Hand([card])])
    
    def double(self):
        if not self.playing:
            return
        self.bet *= 2
        self.double = True

class Dealer:
    def __init__(self):
        self.hand = Hand()
    
    def add_to_hand(self, card):
        self.hand.add_to_hand(card)

class Game:
    def __init__(self, num_players=1):
        self.deck = Deck(3)
        self.players = [Player() for _ in range(num_players)]
        self.dealer = Dealer()
    
    def play_round(self):
        pass