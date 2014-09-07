# to make nice looking print_board
from __future__ import print_function
import random
import cards

class Gameboard(object):
    """
    The Gameboard class holds the contents of the board. Each square can have
    a living and dead unit on it. Nothing can be created on top of another
    living thing. The Gameboard class also keeps track of the board alignment
    and the number of turns that have elapsed. It has functions to create and
    kill creatures, structures, and commanders, and one to cast all the spells.
    """
    def __init__(self, width, height, number_of_players):
        self.width = width
        self.height = height
        self.number_of_players = number_of_players
        self.commanders = []
        self.board = []
        # each spot in the w x h grid should be filled with a living/dead
        # dictionary so that creatures and corpses can share a square
        for row in range(height):
            self.board.append([])
            for column in range(width):
                self.board[row].append({"alive": 0, "dead": 0})

        # get it started
        self.spawn_commanders()

        # alignment determines chances of things occurring
        self.alignment = 0

        # after all commanders have taken their turn, the next round begins
        round_count = 1

        # to be used across the top of the board as it updates
        message = ""

    def print_board(self):
        """
        Just draws out the board in the terminal, with units represented
        as the first letter in their name.
        """
        # always print the alignment above the board
        if self.alignment == 0:
            align = "<none>"
        elif self.alignment > 0:
            align = "Technology %i" % abs(self.alignment)
        elif self.alignment < 0:
            align = "Lifeforce %i" % abs(self.alignment)
        print("ALIGNMENT: %s" % align)

        # this is some formatting that creates a grid for the board, and 
        # prints out the first letter of whatever is on a space.  the letter
        # will be lowercase if it's a corpse.
        print('-' * (self.width * 4 + 1), sep='')
        for row in range(len(self.board)):
            print('|', end='')
            list_of_elements = []
            counter = 0
            for element in self.board[row]:
                if element == 0:
                    list_of_elements.append(0)
                else:
                    list_of_elements.append(element)
            for square in list_of_elements:
                counter += 1
                if counter == self.width:
                    if square["alive"] != 0:
                        print (" {}".format(square["alive"].name[0]), 
                               sep='', end=' ')
                    elif square["dead"] != 0:
                        print (" {}".format(square["dead"].name[0].lower()), 
                               sep='', end=' ')
                    else:
                        print (" {}".format(" "), sep='', end=' ')
                else:
                    if square["alive"] != 0:
                        print (" {}".format(square["alive"].name[0]), 
                               sep='', end=' |')
                    elif square["dead"] != 0:
                        print (" {}".format(square["dead"].name[0].lower()), 
                               sep='', end=' |')
                    else:
                        print (" {}".format(" "), sep='', end=' |')
            print ('|')
            print('-' * (self.width * 4 + 1), sep='')

    def spawn_commanders(self):
        """
        This function takes the number of players on the Gameboard, up to 6,
        and places the commanders on the board in opening squares that are far
        from one another, symmetrically.
        """
        if self.number_of_players == 1:
            # centralize the only player, for testing things
            self.commanders = [cards.Commander() for _ in range(1)]
            for c in self.commanders:
                c.gameboard = self

            self.board[self.height / 2][self.width / 2]["alive"] = \
            self.commanders[0]

            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(self.height / 2, self.width / 2)

        elif self.number_of_players == 2:
            # the players should be far left and right halfway down the board
            self.commanders = [cards.Commander() for _ in range(2)]
            for c in self.commanders:
                c.gameboard = self

            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      self.commanders[0]

            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(int(round(self.height * 4.0 / 10.0)), 
                             int(round(self.width / 15.0)))

            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]\
                      ["alive"] = self.commanders[1]

            self.commanders[1].x, self.commanders[1].y = \
            self.coordinates(int(round(self.height * 4.0 / 10.0)),
                             int(round(self.width * 13.0 / 15.0)))

        elif self.number_of_players == 3:
            # this puts commanders in the bottom left/right corner,
            # and one centrally located along the top
            self.commanders = [cards.Commander() for _ in range(3)]
            for c in self.commanders:
                c.gameboard = self

            self.board[0][self.width / 2]["alive"] = self.commanders[0]
            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(0, self.width / 2)

            self.board[self.height - 1][0]["alive"] = self.commanders[1]
            self.commanders[1].x, self.commanders[1].y = \
            self.coordinates(self.height - 1, 0)

            self.board[self.height - 1][self.width - 1]["alive"] = \
            self.commanders[2]
            self.commanders[2].x, self.commanders[2].y = \
            self.coordinates(self.height - 1, self.width - 1)

        elif self.number_of_players == 4:
            # the players form a rectangle that mimics the board shape
            self.commanders = [cards.Commander() for _ in range(4)]
            for c in self.commanders:
                c.gameboard = self

            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      self.commanders[0]
            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(int(round(self.height / 10.0)),
                             int(round(self.width / 15.0)))

            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      self.commanders[1]
            self.commanders[1].x, self.commanders[1].y = \
            self.coordinates(int(round(self.height / 10.0)),
                             int(round(self.width * 13.0 / 15.0)))

            self.board[self.height - 1]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      self.commanders[2]
            self.commanders[2].x, self.commanders[2].y = \
            self.coordinates(self.height - 1,
                             int(round(self.width / 15.0)))

            self.board[self.height - 1]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      self.commanders[3]
            self.commanders[3].x, self.commanders[3].y = \
            self.coordinates(self.height - 1,
                             int(round(self.width * 13.0 / 15.0)))

        elif self.number_of_players == 5:
            # the commanders are placed in a pentagram copying the 2 player
            # setup, with 1 near the top 3-player commander and 2 along the
            # bottom, at 1/3 intervals
            self.commanders = [cards.Commander() for _ in range(5)]
            for c in self.commanders:
                c.gameboard = self

            self.board[int(round(self.height / 10.0))]\
                      [self.width / 2]["alive"] = self.commanders[0]
            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(int(round(self.height / 10.0)),
                             self.width / 2)

            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      self.commanders[1]
            self.commanders[1].x, self.commanders[1].y = \
            self.coordinates(int(round(self.height * 4.0 / 10.0)),
                             int(round(self.width / 15.0)))

            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      self.commanders[2]
            self.commanders[2].x, self.commanders[2].y = \
            self.coordinates(int(round(self.height * 4.0 / 10.0)),
                             int(round(self.width * 13.0 / 15.0)))

            self.board[self.height - 1]\
                      [int(round(self.width * 4.0 / 15.0))]["alive"] = \
                      self.commanders[3]
            self.commanders[3].x, self.commanders[3].y = \
            self.coordinates(self.height - 1,
                             int(round(self.width * 4.0 / 15.0)))

            self.board[self.height - 1]\
                      [int(round(self.width * 10.0 / 15.0))]["alive"] = \
                      self.commanders[4]
            self.commanders[4].x, self.commanders[4].y = \
            self.coordinates(self.height - 1,
                             int(round(self.width * 10.0 / 15.0)))

        elif self.number_of_players == 6:
            # 6 is a copy of 4, with the top commander from the 5-player
            # setup and one commander symmetrically on the bottom
            self.commanders = [cards.Commander() for _ in range(6)]
            for c in self.commanders:
                c.gameboard = self

            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width / 15))]["alive"] = \
                      self.commanders[0]
            self.commanders[0].x, self.commanders[0].y = \
            self.coordinates(int(round(self.height / 10.0)),
                             int(round(self.width / 15)))

            self.board[int(round(self.height / 10.0))]\
                      [self.width / 2]["alive"] = self.commanders[1]
            self.commanders[1].x, self.commanders[1].y = \
            self.coordinates(int(round(self.height / 10.0)), self.width / 2)

            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      self.commanders[2]
            self.commanders[2].x, self.commanders[2].y = \
            self.coordinates(int(round(self.height / 10.0)),
                             int(round(self.width * 13.0 / 15.0)))

            self.board[self.height - 1]\
                      [int(round(self.width / 15))]["alive"] = \
                      self.commanders[3]
            self.commanders[3].x, self.commanders[3].y = \
            self.coordinates(self.height - 1, int(round(self.width / 15)))

            self.board[self.height - 1][self.width / 2]["alive"] = \
                      self.commanders[4]
            self.commanders[4].x, self.commanders[4].y = \
            self.coordinates(self.height - 1, self.width / 2)

            self.board[self.height - 1]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      self.commanders[5]
            self.commanders[5].x, self.commanders[5].y = \
            self.coordinates(self.height - 1, 
                             int(round(self.width * 13.0 / 15.0)))
            
    def beam_creature(self, x, y, creature):
        #don't beam a creature onto another living creature
        if self.board[self.height - y][x - 1]["alive"] == 0:
            # if the board and the creature share alignments, 
            # give a boost over the normal probability
            r = random.randint(1, 10) / 10.0
            if ((creature.alignment > 0 and self.alignment > 0) or
               (creature.alignment < 0 and self.alignment < 0)):
                success = creature.probability + abs(self.alignment) / 10.0
            else:
                success = creature.probability

            # beam worked, place it on the board
            if success >= r:
                self.message = "SUCCESS"
                self.board[self.height - y][x - 1]["alive"] = creature
                creature.x, creature.y = x, y
            else:
                self.message = "CREATURE FAILURE"
        else:
            print("ALREADY SOMETHING THERE")

    def holo_creature(self, x, y, creature):
        # don't holo onto existing living thing
        if self.board[self.height - y][x - 1]["alive"] == 0:
            # holograms are successful 100% of the time
            self.message = "SUCCESS"
            self.board[self.height - y][x - 1]["alive"] = creature
            creature.holograph = True
            creature.x, creature.y = x, y
        else:
            print("ALREADY SOMETHING THERE")

    def occupant(self, x, y):
        """This function takes a square and returns the living unit on it."""
        return self.board[self.height - y][x - 1]["alive"]

    def coordinates(self, i, j):
        """This function takes array coordinates and returns their x, y."""
        return (j + 1, self.height - i)

    def kill_creature(self, x, y):
        """
        This function takes a square and kills the unit on it. If the unit
        was real, leave a corpse. If hologram, just destroy it.
        """
        if self.occupant(x, y).holograph != True:
            self.board[self.height - y][x - 1]["dead"] = \
            self.board[self.height - y][x - 1]["alive"]
        self.board[self.height - y][x - 1]["alive"] = 0

    def kill_structure(self, x, y):
        """This function takes a square and destroys the structure on it."""
        self.board[self.height - y][x - 1]["alive"] = 0

    def kill_commander(self, x, y, commander):
        """This function takes a square and destroys the commander on it."""
        # self.board[self.height - y][x - 1]["alive"] = 0
        # go through the commander's hand and kill everything
        # go through the commander's creatures and kill each of them
        pass

    def next_round(self):
        """
        This function will determine a round over, and proceed to the next round
        """
        if self.round_count >= 35:
            message = "Game Over, result is DRAW"
        else:
            self.round_count += 1