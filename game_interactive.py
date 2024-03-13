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
    def __init__(self, cards=None):
        if not cards:
            cards = []
        self.cards = cards
        self.value = 0

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
    def __init__(self, id:int, money=100, bet=1):
        self.hands = [Hand()]
        self.hand_idx = 0
        self.money = money
        self.bet = bet
        self.playing = True if money > 0 else False
        self.doubled = False
        self.id = id

    def play(self, dealer_hand: Hand, card: Card): # where the player logic comes in
        if not self.playing:
            print(f'Player {self.id} is not playing.')
            return False
        print(f'Player {self.id} is about to play on hand {self.hands[self.hand_idx]}.')
        move = input('Press h to hit, x to split, s to stay and d to double: ')
        match move:
            case 'h':
                self.hit(card)
            case 'd':
                self.double()
                card.show = False
                self.hit(card)
            case 'x':
                self.split()
            case 's':
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
            self.hands.extend([Hand([card]), Hand([card])])
            print(f'Player {self.id}\'s new hand is {self.hands}.')
        else:
            print('Can not split.')
    
    def double(self):
        if not self.playing:
            return
        self.bet *= 2
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
            player.bet = int(input(f'Place your bet, Player {player.id}: '))
        self.setup()
        print(f'Dealer hand is {self.dealer.hand}.')
        for player in self.players:
            print(f'Player {player.id}\'s hand is {player.hands}')
        time.sleep(2)
        for player in self.players:
            print(f'-------------------- PLAYER {player.id}\'S TURN --------------------')
            playing = True
            while playing:
                playing = player.play(None, self.dealer.deal())
        print(f'-------------------- DEALING TIME --------------------')
        dealer_score = self.dealer.play()
        for player in self.players:
            for hand in player.hands:
                showed = hand.reveal()
                if showed:
                    print(f'Player hand after revealing card(s) is {hand}')
                value = hand.compute_value()
                if value < 21 and value > dealer_score:
                    player.money += player.bet
                    print(f'Player {player.id} made {player.bet} bucks! Player now has {player.money} money left.')
                elif value < 21 and value == dealer_score:
                    print(f'Player {player.id} stood.')
                else:
                    player.money -= player.bet
                    print(f'Player {player.id} lost {player.bet} bucks! Player now has {player.money} money left.')
            time.sleep(1)
        for player in self.players:
            player.reset()
        self.dealer.reset()
        print(f'-------------------- ROUND END --------------------')

if __name__ == '__main__':
    game = Game(2)
    for _ in range(2):
        game.play_round()