import random
import board
import cards

# players = random.randint(2, 6)
players = 2
gameboard = board.Gameboard(players)
seer = cards.Drone()
blocker = cards.Droid()
seer.gameboard = gameboard
gameboard.beam_creature(1, 10, seer)
gameboard.holo_creature(1, 8, blocker)
gameboard.holo_creature(2, 10, blocker)
gameboard.holo_creature(2, 9, blocker)



gameboard.print_board()
print seer.squares_seen()


# for turn in range(5):
#     for player in range(players):
#         gameboard.commanders[player].choose_card()
#     for player in range(players):
#         gameboard.commanders[player].target_card()
#     for player in range(players):
#         gameboard.commanders[player].move()