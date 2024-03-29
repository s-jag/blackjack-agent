import random
import time
from enum import Enum

class Actions(Enum):
    HIT = 'HIT'
    DOUBLE = 'DOUBLE'
    SPLIT = 'SPLIT'
    STAY = 'STAY'

# from strategies import BasicStrategy

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
    
class BasicStrategy:
    def is_soft_hand(self, player_hand: Hand):
        return any(card.value == 'A' for card in player_hand.cards) and player_hand.compute_value() + 10 <= 21

    def is_pair(self, player_hand: Hand):
        return len(player_hand.cards) == 2 and player_hand.cards[0].value == player_hand.cards[1].value

    def optimal_move(self, player_hand: Hand, dealer_hand: Hand):
        dealer_value = dealer_hand.compute_value()
        hand_value = player_hand.compute_value()

        # Pair handling
        if self.is_pair(player_hand=player_hand):
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
        if self.is_soft_hand(player_hand=player_hand):
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
            print('here')
            print('HIT' if dealer_value >= 7 else 'STAND')
            return 'HIT' if dealer_value >= 7 else 'STAND'
        return 'HIT'  


class Player:
    def __init__(self, id:int, money=100, bet=1, strategy=None):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.money = money
        self.bet = bet
        self.playing = True if money > 0 else False
        self.doubled = False
        self.id = id
        self.strategy = BasicStrategy()

    def set_bet(self, amount: int):
        self.bet = amount
        for hand in self.hands:
            hand.bet = amount

    def play(self, dealer_hand: Hand, card: Card): # where the player logic comes in
        if not self.playing:
            print(f'Player {self.id} is not playing.')
            return False
        print(f'Player {self.id} is about to play on hand {self.hands[self.hand_idx]}.')
        current_hand = self.hands[self.hand_idx]
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
        time.sleep(1)
        return True

    def is_playing(self):
        return self.playing
    
    def add_to_hand(self, card: Card):
        return self.hands[self.hand_idx].add_to_hand(card)
    
    def reset(self):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.doubled = False
        self.playing = True if self.money > 0 else False

    def hit(self, card: Card):
        if not self.playing:
            return
        bust = self.add_to_hand(card)
        print(f'Player {self.id} has chosen to hit on {card}. Total score is {self.hands[self.hand_idx].compute_value()}. Hand is {self.hands}.')
        time.sleep(1)
        if bust:
            print(f'Player\'s hand number {self.hand_idx + 1} went bust. Player loses {self.bet} money. Player dumb.')
            self.hand_idx += 1
            if self.hand_idx >= len(self.hands):
                self.hand_idx = 0
                self.playing = False
        if self.doubled:
            self.stand()
    
    def stand(self):
        print(f'Player {self.id} has chosen to stand on hand {self.hand_idx + 1}. Total score is {self.hands[self.hand_idx].compute_value()}. Hand is {self.hands}.')
        self.hand_idx += 1
        if self.hand_idx >= len(self.hands):
            self.hand_idx = 0
            self.playing = False

    def split(self):
        if not self.playing:
            return
        current_hand = self.hands[self.hand_idx]
        if len(current_hand.cards) == 2 and current_hand.cards[0] == current_hand.cards[1]:
            print(f'Player {self.id} is splitting...')
            card = self.hands.pop(self.hand_idx).cards[0]
            self.hands.extend([Hand([card], self.bet), Hand([card], self.bet)])
            print(f'Player {self.id}\'s new hand is {self.hands}.')
        else:
            print('Can not split.')
    
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
        if showed:
            print(f'Dealer hand after revealing card(s) is {self.hand}')
        while self.hand.compute_value() < 17:
            card = self.deal()
            self.hand.add_to_hand(card)
            print(f'Dealer added {card} to their hand. Dealer hand is {self.hand}.')
            time.sleep(1)
        print(f'Dealer final hand is {self.hand}. The total score is {self.hand.compute_value()}.')
        if self.hand.compute_value() > 21:
            print('Dealer went bust!')
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
        print(f'-------------------- ROUND START --------------------')
        for player in self.players:
            player.set_bet(int(input(f'Place your bet, Player {player.id}: ')))
        self.setup()
        print(f'Dealer hand is {self.dealer.hand}.')
        for player in self.players:
            print(f'Player {player.id}\'s hand is {player.hands}')
        time.sleep(2)
        for player in self.players:
            print(f'-------------------- PLAYER {player.id}\'S TURN --------------------')
            playing = True
            while playing:
                playing = player.play(self.dealer.hand, self.dealer.deal())
        print(f'-------------------- DEALING TIME --------------------')
        dealer_score = self.dealer.play()
        for player in self.players:
            for hand in player.hands:
                showed = hand.reveal()
                if showed:
                    print(f'Player hand after revealing card(s) is {hand}')
                value = hand.compute_value()
                if value <= 21 and value > dealer_score:
                    player.money += hand.bet
                    print(f'Player {player.id} made {hand.bet} bucks! Player now has {player.money} money left.')
                elif value <= 21 and value == dealer_score:
                    print(f'Player {player.id} pushed.')
                else:
                    player.money -= hand.bet
                    print(f'Player {player.id} lost {hand.bet} bucks! Player now has {player.money} money left.')
            time.sleep(1)
        for player in self.players:
            player.reset()
        self.dealer.reset()
        print(f'-------------------- ROUND END --------------------')

if __name__ == '__main__':
    game = Game(2)
    for _ in range(2):
        game.play_round()