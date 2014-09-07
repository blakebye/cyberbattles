import random

import board

players = random.randint(1, 6)
gameboard = board.Gameboard(15, 10, players)

for player_number in range(players):
    print gameboard.commanders[player_number].hand
    for card in gameboard.commanders[player_number].hand:
        print card.name
        gameboard.commanders[player_number].play_card(card)

gameboard.print_board()