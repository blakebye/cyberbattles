# to make nice looking print_board
from __future__ import print_function
import random
import creatures as c
import structures as s
import spells as sp

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
        self.board = []

        # each spot in the w x h grid should be filled with a living/dead
        # dictionary so that creatures and corpses can share a square
        for row in range(height):
            self.board.append([])
            for column in range(width):
                self.board[row].append({"alive": 0, "dead": 0})

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
            self.board[self.height / 2][self.width / 2]["alive"] = c.Commander()

        elif self.number_of_players == 2:
            # the players should be far left and right halfway down the board
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()

        elif self.number_of_players == 3:
            # this puts commanders in the bottom left/right corner,
            # and one centrally located along the top
            self.board[self.height - 1][0]["alive"] = c.Commander()
            self.board[self.height - 1][self.width - 1]["alive"] = c.Commander()
            self.board[0][self.width / 2]["alive"] = c.Commander()

        elif self.number_of_players == 4:
            # the players form a rectangle that mimics the board shape
            self.board[self.height - 1]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      c.Commander()
            self.board[self.height - 1]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()

        elif self.number_of_players == 5:
            # the commanders are placed in a pentagram copying the 2 player
            # setup, with 1 near the top 3-player commander and 2 along the
            # bottom, at 1/3 intervals
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [self.width / 2]["alive"] = \
                      c.Commander()
            self.board[self.height - 1]\
                      [int(round(self.width * 4.0 / 15.0))]["alive"] = \
                      c.Commander()
            self.board[self.height - 1]\
                      [int(round(self.width * 10.0 / 15.0))]["alive"] = \
                      c.Commander()

        elif self.number_of_players == 6:
            # 6 is a copy of 4, with the top commander from the 5-player
            # setup and one commander symmetrically on the bottom
            self.board[self.height - 1]\
                      [int(round(self.width / 15))]["alive"] = \
                      c.Commander()
            self.board[self.height - 1]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width / 15))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height / 10.0))]\
                      [self.width / 2]["alive"] = \
                      c.Commander()
            self.board[self.height - 1][self.width / 2]["alive"] = \
                      c.Commander()
            

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
        else:
            print("ALREADY SOMETHING THERE")

    def create_structure(self, x, y, structure):
        # if the board alignment is technology, give the structure
        # a boost over it's normal probability to be created
        r = random.randint(1, 10) / 10.0
        if self.alignment > 0:
            success = structure.probability + self.alignment / 10.0
        else:
            success = structure.probability
        if success >= r:
            # fortress is a one square structure
            if isinstance(structure, s.Fortress):
                if self.board[self.height - y][x - 1]["alive"] == 0:
                    self.board[self.height - y][x - 1]["alive"] = structure

            # gun turret and subspace beacon share a creation pattern
            elif (isinstance(structure, s.GunTurret) or
                  isinstance(structure, s.SubspaceBeacon)):
                for i, j in ((x - 1, y), (x + 1, y), (x, y + 2), (x, y - 2), 
                             (x - 2, y + 2), (x + 2, y + 2), (x - 2, y - 2), 
                             (x + 2, y - 2)):
                    if (j > 0 and i > 0 and 
                        j <= self.height and i <= self.width):
                        if self.board[self.height - j][i - 1]["alive"] == 0:
                            self.board[self.height - j][i - 1]["alive"] = structure

            # force field has a unique creation pattern
            elif isinstance(structure, s.ForceField):
                for i, j in ((x - 2, y + 1), (x - 2, y + 2), (x - 1, y + 2), 
                             (x + 2, y + 1), (x + 2, y + 2), (x + 1, y + 2),
                             (x - 2, y - 1), (x - 2, y - 2), (x - 1, y - 2),
                             (x + 2, y - 1), (x + 2, y - 2), (x + 1, y - 2)):
                    if (j > 0 and i > 0 and 
                        j <= self.height and i <= self.width):
                        if self.board[self.height - j][i - 1]["alive"] == 0:
                            self.board[self.height - j][i - 1]["alive"] = structure
        else:
            self.message = "STRUCTURE FAILURE"

    def occupant(self, x, y):
        """This function takes a square and returns the living unit on it."""
        return self.board[self.height - y][x - 1]["alive"]

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
        pass

    def upgrade_commander(self, x, y, up):
        """
        This function takes a square and an upgrade type and upgrades the
        commander on that square with that upgrade.
        """
        if isinstance(self.occupant(x, y), c.Commander):
            self.occupant(x, y).upgrade(up)

    def cast_spell(self, x, y, spell):
        """
        This function takes a square and a spell and casts that spell onto that
        square.
        """
        # if the spell and board alignment are the same, give the spell
        # a bonus chance to be cast successfully
        r = random.randint(1, 10) / 10.0
        if ((spell.alignment > 0 and self.alignment > 0) or
            (spell.alignment < 0 and self.alignment < 0)):
            success = spell.probability + abs(self.alignment) / 10.0
        else:
            success = spell.probability
        if success >= r:
            # holodetect will instantly kill a hologram on the targetted square
            if isinstance(spell, sp.HoloDetect):
                if self.board[self.height - y][x - 1]["alive"].holograph == True:
                    self.board[self.height - y][x - 1]["alive"] = 0
                else:
                    pass

            # mutate will change a creature on the targetted
            # square into another random creature
            elif isinstance(spell, sp.Mutate):
                # requires all creatures to be implemented as cards
                pass

            # hypnotize will change the owner of
            # a creature on the targetted square
            elif isinstance(spell, sp.Hypnotize):
                # requires creatures be implemented as commanders possession
                pass

            # resurrect will turn a corpse into a living creature again
            elif isinstance(spell, sp.Resurrect):
                self.board[self.height - y][x - 1]["alive"] = \
                self.board[self.height - y][x - 1]["dead"]

                # don't forget to remove the corpse
                self.board[self.height - y][x - 1]["dead"] = 0

            # disrupt has a small chance to instantly kill a creature
            elif isinstance(spell, sp.Disrupt):
                r = random.randint(5, 13)
                if (self.occupant(x, y).resist +
                    self.occupant(x, y).defense) < r:
                    self.kill_creature(x, y)

            # disrupt has a medium chance to instantly kill a creature
            elif isinstance(spell, sp.Disintegrate):
                r = random.randint(7, 17)
                if (self.occupant(x, y).resist +
                    self.occupant(x, y).defense) < r:
                    self.kill_creature(x, y)

            # emp can instantly kill any tech aligned creature if it succeeds
            # it can also target a commander to kill all his tech units
            elif isinstance(spell, sp.EMP):
                if self.occupant(x, y).alignment > 0:
                    self.kill_creature(x, y)

            # virus can instantly kill any life aligned creature if it succeeds
            # it can also target a commander to kill all his life units
            elif isinstance(spell, sp.Virus):
                if self.occupant(x, y).alignment < 0:
                    self.kill_creature(x, y)

            # teleport can move your commander up to 7 squares away
            elif isinstance(spell, sp.Teleport):
                # teleport is tricky. need to make line of sight code
                pass

            # align isn't really a spell, but instead of making a whole
            # module for it, it fits well here to alter the board.
            elif isinstance(spell, sp.Align):
                if spell.direction == "Technology":
                    self.align_tech(spell.level)
                if spell.direction == "Lifeforce":
                    self.align_life(spell.level)
        else:
            self.message("SPELL FAILURE")

    def align_life(self, level):
        """this just works with the Align spell to change the board alignment"""
        self.alignment -= 1 * level

    def align_tech(self, level):
        """this just works with the Align spell to change the board alignment"""
        self.alignment += 1 * level

    def next_round(self):
        """
        This function will determine a round over, and proceed to the next round
        """
        if self.round_count >= 35:
            message = "Game Over, result is DRAW"
        else:
            self.round_count += 1