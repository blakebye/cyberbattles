import random
import board
import cards

players = random.randint(2, 6)
gameboard = board.Gameboard(players)

for turn in range(5):
    for player in range(players):
        gameboard.commanders[player].choose_card()
    for player in range(players):
        gameboard.commanders[player].target_card()
    for player in range(players):
        gameboard.commanders[player].move()