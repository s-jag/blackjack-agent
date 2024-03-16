import random
import time

SUITS = ['♠', '♥', '♦', '♣']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
    def __init__(self, suit: str, value: str, show=True):
        self.suit = suit
        self.value = value
        self.show = show

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return f'{self.suit} {self.value}' if self.show else 'X'
    
class Deck:
    def __init__(self, number_of_decks=3):
        one_deck = [Card(s, v) for s in SUITS for v in VALUES]
        self.cards = []
        for _ in range(number_of_decks):
            self.cards += one_deck
        random.shuffle(self.cards)

    def draw(self, show=True):
        card = self.cards.pop()
        card.show = show
        return card
    
class Hand:
    def __init__(self, cards=None, bet=0):
        if not cards:
            cards = []
        self.cards = cards
        self.value = 0
        self.bet = bet #for players only

    def clear(self):
        self.cards = []
        self.value = 0
    
    def reveal(self):
        showed = False
        for card in self.cards:
            if not card.show:
                showed = True
            card.show = True
        return showed

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
            if not card.show:
                continue
            if card.value == 'A':
                value_high += 11
                value_low += 1
                continue
            value_high += min(1 + VALUES.index(card.value), 10)
            value_low += min(1 + VALUES.index(card.value), 10)
        self.value = value_high if value_high <= 21 else value_low
        return self.value
    
    def __str__(self):
        return '[' + ', '.join(map(str, self.cards)) + ']'
    
    def __repr__(self):
        return '[' + ', '.join(map(str, self.cards)) + ']'

class Player:
    def __init__(self, id:int, money=2000, bet=1, strategy=None):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.money = money
        self.bet = bet
        # self.playing = True if money > 0 else False
        self.playing = True
        self.doubled = False
        self.id = id
        self.strategy = strategy

    def set_bet(self, amount: int):
        self.bet = amount
        for hand in self.hands:
            hand.bet = amount

    def play(self, dealer_hand: Hand, card: Card): # where the player logic comes in
        if not self.playing:
            return False
        current_hand = self.hands[self.hand_idx]
        if not self.strategy:
            return False
        move = self.strategy.optimal_move(player_hand=current_hand, dealer_hand=dealer_hand)
        if move == 'HIT':
            self.hit(card)
        elif move == 'DOUBLE':
            self.double()
            card.show = False
            self.hit(card)
        elif move == 'SPLIT':
            self.split()
        elif move == 'STAND':
            self.stand()
        return True

    def is_playing(self):
        return self.playing
    
    def add_to_hand(self, card: Card):
        return self.hands[self.hand_idx].add_to_hand(card)
    
    def reset(self):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.doubled = False
        # self.playing = True if self.money > 0 else False
        self.playing = True

    def hit(self, card: Card):
        if not self.playing:
            return
        bust = self.add_to_hand(card)
        if bust:
            self.hand_idx += 1
            if self.hand_idx >= len(self.hands):
                self.hand_idx = 0
                self.playing = False
        if self.doubled:
            self.stand()
    
    def stand(self):
        self.hand_idx += 1
        if self.hand_idx >= len(self.hands):
            self.hand_idx = 0
            self.playing = False

    def split(self):
        if not self.playing:
            return
        current_hand = self.hands[self.hand_idx]
        if len(current_hand.cards) == 2 and current_hand.cards[0] == current_hand.cards[1]:
            card = self.hands.pop(self.hand_idx).cards[0]
            self.hands.extend([Hand([card], self.bet), Hand([card], self.bet)])
        else:
            pass
    
    def double(self):
        if not self.playing:
            return
        self.hands[self.hand_idx].bet *= 2
        self.doubled = True

class Dealer:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.hand = Hand()
    
    def add_to_hand(self, card):
        self.hand.add_to_hand(card)

    def deal(self, show=True):
        return self.deck.draw(show)

    def reset(self):
        self.hand = Hand()
    
    def play(self):
        showed = self.hand.reveal()
        while self.hand.compute_value() < 17:
            card = self.deal()
            self.hand.add_to_hand(card)
        if self.hand.compute_value() > 21:
            self.hand.clear()
        return self.hand.compute_value()


class Game:
    def __init__(self, num_players=1):
        self.deck = Deck(3)
        self.players = [Player(id=id) for id in range(num_players)]
        self.dealer = Dealer(self.deck)

    def setup(self):
        for player in self.players:
            player.add_to_hand(self.dealer.deal())
        self.dealer.add_to_hand(self.dealer.deal())

        for player in self.players:
            player.add_to_hand(self.dealer.deal())
        self.dealer.add_to_hand(self.dealer.deal(False))

    def play_round(self):
        if len(self.deck.cards) < 30:
            self.deck = Deck(3)
            self.dealer.deck = self.deck
        for player in self.players:
            player.set_bet(1)
        self.setup()
        for player in self.players:
            playing = True
            while playing:
                playing = player.play(self.dealer.hand, self.dealer.deal())
        dealer_score = self.dealer.play()
        for player in self.players:
            for hand in player.hands:
                showed = hand.reveal()
                value = hand.compute_value()
                if value <= 21 and value > dealer_score:
                    player.money += hand.bet
                elif value <= 21 and value == dealer_score:
                    pass
                else:
                    player.money -= hand.bet
        for player in self.players:
            player.reset()
        self.dealer.reset()