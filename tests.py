import board
gameboard = board.Gameboard(15, 10, 5)
gameboard.spawn_commanders()
print gameboard.commander1
print gameboard.commander1.hand[6].commander

gameboard.print_board()