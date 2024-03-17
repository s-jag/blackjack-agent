from game_core_entities import Game
from strategies import BasicStrategy, HiLoCardCountingStrategy

# if __name__ == '__main__':
#     game = Game(2)
#     for player in game.players:
#         player.strategy = BasicStrategy
#     for _ in range(100000):
#         game.play_round()
#     for player in game.players:
#         print(f'Player {player.id}: {player.money}')


if __name__ == '__main__':
    game = Game(num_players=2)  # Assuming you want to simulate the game with 2 players
    
    # Assign the HiLoCardCountingStrategy to each player
    for player in game.players:
        player.strategy = HiLoCardCountingStrategy(base_bet=1)
    
    # Run the simulation for 10,000 rounds
    for _ in range(100000):
        # Reset the count if a new deck is used
        if len(game.deck.cards) < 30:  # Example threshold to reshuffle
            for player in game.players:
                player.strategy.reset_count()  # Make sure to implement this method
        
        # Adjust bets based on the current count
        for player in game.players:
            # print(player.strategy.running_count)
            player.strategy.update_true_count()
            player.set_bet(player.strategy.adjust_bet_based_on_count())
            # print(player.strategy.adjust_bet_based_on_count())
        
        # Play a round
        game.play_round()
    
    # Output results
    for player in game.players:
        print(f'Player {player.id}: {player.money}')