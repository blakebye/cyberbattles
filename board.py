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
    def __init__(self, number_of_players):
        # assign the number of players so the board knows
        self.number_of_players = number_of_players

        # alignment (toward technology/lifeforce) will give
        # increased chances that similarly aligned things will occur
        self.alignment = 0

        # each spot in the w x h grid should be filled with a living/dead
        # dictionary so that creatures and corpses can share a square without
        # conflict
        self.board = [[{"alive": 0, "dead": 0} for x in range(15)]
                                               for y in range(10)]

        # put players on the board
        self.commanders = self.spawn_commanders()

        # after all commanders have taken their turn, the next round begins
        self.round = 1

        # status to be used across the top of the board as it updates
        self.message = "CYBERBATTLES"

    def print_board(self):
        """
        Draws out the board in the terminal, with units represented
        as the first letter in their name. Also prints the alignment of the
        board and the last status message, which may indicate someone's turn
        or a spell success.
        """

        # display the alignment properly
        if self.alignment == 0:
            align = "<none>"
        elif self.alignment > 0:
            align = "Technology %i" % abs(self.alignment)
        elif self.alignment < 0:
            align = "Lifeforce %i" % abs(self.alignment)

        # always print out the message and alignment above the board
        print("%s - ALIGNMENT: %s" % (self.message, align))

        # this is some formatting that creates a grid for the board, and 
        # prints out the first letter of whatever is on a space.  the letter
        # will be lowercase if it's a corpse.

        # top border
        print('-' * (15 * 4 + 1), sep='')

        # for every row
        for row in range(len(self.board)):
            # left border
            print('|', end='')

            # we'll populate this list with the whole row at once
            list_of_elements = []
            for element in self.board[row]:
                list_of_elements.append(element)

            # go through each element
            for element in list_of_elements:
                # if there's something alive there, print out the first letter
                if element["alive"] != 0:
                    print (" {}".format(element["alive"].name[0]), 
                           sep='', end=" |")

                # if there's a corpse, print out a lowercase first letter
                elif element["dead"] != 0:
                    print (" {}".format(element["dead"].name[0].lower()), 
                           sep='', end=" |")

                # nothing is on the square at all, print a space
                else:
                    print (" {}".format(" "), sep='', end=" |")
            # next line
            print("")
            # bottom border for every line
            print('-' * (15 * 4 + 1), sep='')

    def spawn_commander(self, commander, i, j):
        """
        This function is a helper to spawn_commanders that just cleans it up a
        bit.  It takes a commander and a pair of indices, and then places that
        commander at those indices and gives the commander his coordinates.
        """
        self.occupy(j + 1, 10 - i, commander)
        commander.x, commander.y = (j + 1, 10 - i)

    def spawn_commanders(self):
        """
        This function takes the number of players on the Gameboard, up to 6,
        and places the commanders on the board in opening squares that are far
        from one another, symmetrically.
        """

        # create a commander for each player
        commanders = [cards.Commander() for x in 
                      range(self.number_of_players)]

        # assign each commander its name and board controller
        for c in commanders:
            c.gameboard = self
            c.name = "COMMANDER %i" % (commanders.index(c) + 1)

        # assign very specific starting positions based on number of players
        if self.number_of_players == 1:
            # centralize the only player, for testing things
            self.spawn_commander(commanders[0], 4, 7)
        elif self.number_of_players == 2:
            # the players should be far left and right halfway down the board
            self.spawn_commander(commanders[0], 4, 1)
            self.spawn_commander(commanders[1], 4, 13)
        elif self.number_of_players == 3:
            # this puts commanders in the bottom left/right corner,
            # and one centrally located along the top
            self.spawn_commander(commanders[0], 0, 7)
            self.spawn_commander(commanders[1], 9, 0)
            self.spawn_commander(commanders[2], 9, 14)
        elif self.number_of_players == 4:
            # the players form a rectangle that mimics the board shape
            self.spawn_commander(commanders[0], 1, 1)
            self.spawn_commander(commanders[1], 1, 13)
            self.spawn_commander(commanders[2], 9, 1)
            self.spawn_commander(commanders[3], 9, 13)
        elif self.number_of_players == 5:
            # the commanders are placed in a pentagram copying the 2 player
            # setup, with 1 near the top 3-player commander and 2 along the
            # bottom, at 1/3 intervals
            self.spawn_commander(commanders[0], 1, 7)
            self.spawn_commander(commanders[1], 4, 1)
            self.spawn_commander(commanders[2], 4, 13)
            self.spawn_commander(commanders[3], 9, 4)
            self.spawn_commander(commanders[4], 9, 10)
        elif self.number_of_players == 6:
            # 6 is a copy of 4, with the top commander from the 5-player
            # setup and one commander symmetrically on the bottom
            self.spawn_commander(commanders[0], 1, 1)
            self.spawn_commander(commanders[1], 1, 7)
            self.spawn_commander(commanders[2], 1, 13)
            self.spawn_commander(commanders[3], 9, 1)
            self.spawn_commander(commanders[4], 9, 7)
            self.spawn_commander(commanders[5], 9, 13)

        return commanders
            
    def beam_creature(self, x, y, creature):
        self.message = "BEAMED %s SUCCESSFULLY" % creature.name.upper()
        self.occupy(x, y, creature)
        creature.x, creature.y = x, y
        creature.gameboard = self


    def holo_creature(self, x, y, creature):
        # holograms are successful 100% of the time
        self.message = "BEAMED %s SUCCESSFULLY" % creature.name.upper()
        self.occupy(x, y, creature)
        creature.hologram = True
        creature.x, creature.y = x, y
        creature.gameboard = self

    def occupant(self, x, y):
        """This function takes a square and returns the living unit on it."""
        return self.board[10 - y][x - 1]["alive"]

    def dead_occupant(self, x, y):
        """This function takes a square and returns the living unit on it."""
        return self.board[10 - y][x - 1]["dead"]

    def occupy(self, x, y, unit):
        """This function takes a square and an object and places it there."""
        self.board[10 - y][x - 1]["alive"] = unit

    def dead_occupy(self, x, y, unit):
        """This function takes a square and an object and places it there."""
        self.board[10 - y][x - 1]["dead"] = unit

    def kill_creature(self, x, y):
        """
        This function takes a square and kills the unit on it. If the unit
        was real, leave a corpse. If hologram, just destroy it.
        """
        dead_creature = self.occupant(x, y)
        dead_creature.commander.dead_creatures.append(dead_creature)
        dead_creature.commander.creatures.remove(dead_creature)
        if dead_creature.hologram != True:
            self.dead_occupy(x, y, dead_creature)
        self.occupy(x, y, 0)


    def kill_structure(self, x, y):
        """This function takes a square and destroys the structure on it."""
        self.board[10 - y][x - 1]["alive"] = 0

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
        for commander in self.commanders:
            for creature in commander.creatures:
                creature.moved = False
        if self.round >= 35:
            message = "Game Over, result is DRAW"
        else:
            self.round += 1