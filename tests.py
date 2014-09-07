import board
gameboard = board.Gameboard(15, 10, 5)
gameboard.spawn_commanders()

i = 0
for x in gameboard.occupant(5, 1).hand:
    i += 1
    print "{}".format(x) ,
    if i % 3 == 0:
        print

gameboard.print_board()