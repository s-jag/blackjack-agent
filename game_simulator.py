from game_core_entities import Game
from strategies import BasicStrategy

if __name__ == '__main__':
    game = Game(2)
    for player in game.players:
        player.strategy = BasicStrategy
    for _ in range(100000):
        game.play_round()
    for player in game.players:
        print(f'Player {player.id}: {player.money}')