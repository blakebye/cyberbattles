import random
import board
import cards

# players = random.randint(1, 6)
players = 2
gameboard = board.Gameboard(players)
d = cards.Drone()
d.commander = gameboard.commanders[1]
d.gameboard = gameboard
gameboard.commanders[1].creatures.append(d)
gameboard.beam_creature(7, 7, d)

while gameboard.round < 35:
    # select card
    for player_number in range(players):
        player = gameboard.commanders[player_number]
        player.play_card()

    # target card, if necessary
    for player_number in range(players):
        pass

    # move creatures
    for player_number in range(players):
        gameboard.commanders[player_number].move()

    gameboard.next_round()