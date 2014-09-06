from __future__ import print_function
import random
import creatures as c
import structures as s
import spells as sp

class Gameboard(object):
    def __init__(self, width, height, number_of_players):
        self.width = width
        self.height = height
        self.number_of_players = number_of_players
        self.board = []
        for row in range(height):
            self.board.append([])
            for column in range(width):
                self.board[row].append({"alive": 0, "dead": 0})
        self.alignment = 0
        round_count = 1
        message = ""

    def print_board(self):
        if self.alignment == 0:
            align = "<none>"
        elif self.alignment > 0:
            align = "Technology %i" % abs(self.alignment)
        elif self.alignment < 0:
            align = "Lifeforce %i" % abs(self.alignment)
        print("ALIGNMENT: %s" % align)
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
        if self.number_of_players == 1:
            self.board[self.height / 2][self.width / 2]["alive"] = c.Commander()

        elif self.number_of_players == 2:
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width / 15.0))]["alive"] = \
                      c.Commander()
            self.board[int(round(self.height * 4.0 / 10.0))]\
                      [int(round(self.width * 13.0 / 15.0))]["alive"] = \
                      c.Commander()

        elif self.number_of_players == 3:
            self.board[self.height - 1][0]["alive"] = c.Commander()
            self.board[self.height - 1][self.width - 1]["alive"] = c.Commander()
            self.board[0][self.width / 2]["alive"] = c.Commander()

        elif self.number_of_players == 4:
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
        if self.board[self.height - y][x - 1]["alive"] == 0:
            r = random.randint(1, 10) / 10.0
            if creature.probability >= r:
                self.message = "SUCCESS"
                self.board[self.height - y][x - 1]["alive"] = creature
            else:
                self.message = "FAILURE"

    def holo_creature(self, x, y, creature):
        if self.board[self.height - y][x - 1]["alive"] == 0:
            self.message = "SUCCESS"
            self.board[self.height - y][x - 1]["alive"] = creature
            creature.holograph = True

    def create_structure(self, x, y, structure):
        r = random.randint(1, 10) / 10.0
        if structure.probability > r:
            if isinstance(structure, s.Fortress):
                if self.board[self.height - y][x - 1]["alive"] == 0:
                    self.board[self.height - y][x - 1]["alive"] = structure

            elif (isinstance(structure, s.GunTurret)):
                for i, j in ((x - 1, y), (x + 1, y), (x, y + 2), (x, y - 2), 
                             (x - 2, y + 2), (x + 2, y + 2), (x - 2, y - 2), 
                             (x + 2, y - 2)):
                    if (j > 0 and i > 0 and 
                        j <= self.height and i <= self.width):
                        if self.board[self.height - j][i - 1]["alive"] == 0:
                            self.board[self.height - j][i - 1]["alive"] = structure

            elif (isinstance(structure, s.SubspaceBeacon)):
                for i, j in ((x - 1, y), (x + 1, y), (x, y + 2), (x, y - 2), 
                             (x - 2, y + 2), (x + 2, y + 2), (x - 2, y - 2), 
                             (x + 2, y - 2)):
                    if (j > 0 and i > 0 and 
                        j <= self.height and i <= self.width):
                        if self.board[self.height - j][i - 1]["alive"] == 0:
                            self.board[self.height - j][i - 1]["alive"] = structure

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
            self.message = "FAILURE"

    def check_occupancy(self, x, y):
        return self.board[self.height - y][x - 1]["alive"]

    def check_dead_creature(self, x, y):
        return self.board[self.height - y][x - 1]["dead"]

    def kill_creature(self, x, y):
        if self.check_occupancy(x, y).holograph != True:
            self.board[self.height - y][x - 1]["dead"] = \
            self.board[self.height - y][x - 1]["alive"]
        self.board[self.height - y][x - 1]["alive"] = 0

    def kill_structure(self, x, y):
        self.board[self.height - y][x - 1]["alive"] = 0

    def kill_commander(self, x, y, commander):
        self.board[self.height - y][x - 1]["alive"] = 0

    def upgrade_commander(self, x, y, up):
        if isinstance(self.check_occupancy(x, y), c.Commander):
            self.check_occupancy(x, y).upgrade(up)

    def cast_spell(self, x, y, spell):
        r = random.randint(1, 10) / 10.0
        if spell.probability > r:
            if isinstance(spell, sp.HoloDetect):
                if self.board[self.height - y][x - 1]["alive"].holograph == True:
                    self.board[self.height - y][x - 1]["alive"] = 0
                else:
                    pass
            elif isinstance(spell, sp.Mutate):
                # requires all creatures to be implementes as cards
                pass
            elif isinstance(spell, sp.Hypnotize):
                # requires commanders be implemented
                pass

            elif isinstance(spell, sp.Resurrect):
                self.board[self.height - y][x - 1]["alive"] = \
                self.board[self.height - y][x - 1]["dead"]

                self.board[self.height - y][x - 1]["dead"] = 0

            elif isinstance(spell, sp.Disrupt):
                r = random.randint(5, 13)
                if (self.check_occupancy(x, y).resist +
                    self.check_occupancy(x, y).defense) < r:
                    self.kill_creature(x, y)

            elif isinstance(spell, sp.Disintegrate):
                r = random.randint(6, 17)
                if (self.check_occupancy(x, y).resist +
                    self.check_occupancy(x, y).defense) < r:
                    self.kill_creature(x, y)

            elif isinstance(spell, sp.EMP):
                if self.check_occupancy(x, y).alignment > 0:
                    self.kill_creature(x, y)

            elif isinstance(spell, sp.Virus):
                if self.check_occupancy(x, y).alignment < 0:
                    self.kill_creature(x, y)

            elif isinstance(spell, sp.Teleport):
                # requires commander be implemented
                pass

            elif isinstance(spell, sp.Align):
                if spell.direction == "Technology":
                    self.align_tech(spell.level)
                if spell.direction == "Lifeforce":
                    self.align_life(spell.level)
        else:
            self.message("FAILURE")

    def align_life(self, level):
        # LIFE WILL BE NEGATIVE
        self.alignment -= 1 * level

    def align_tech(self, level):
        # TECH WILL BE POSITIVE
        self.alignment += 1 * level

    def end_round(self):
        if self.round_count >= 35:
            message = "Game Over, result is DRAW"
        else:
            self.round_count += 1