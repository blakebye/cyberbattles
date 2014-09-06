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
        print(' ', sep='', end='')
        print('-' * (self.width * 2), sep='')
        for row in range(len(self.board)):
            print('|', end='')
            list_of_elements = []
            for element in self.board[row]:
                if element == 0:
                    list_of_elements.append(0)
                else:
                    list_of_elements.append(element)
            for square in list_of_elements:
                if square["alive"] != 0:
                    print ("{}".format(square["alive"].name[0]), 
                           sep='', end=' ')
                elif square["dead"] != 0:
                    print ("{}".format(square["dead"].name[0].lower()), 
                           sep='', end=' ')
                else:
                    print ("{}".format(" "), sep='', end=' ')
            print ('|')
        print(' ', sep='', end='')
        print('-' * (self.width * 2), sep='')

    def spawn_commanders(self):
        if number_of_players == 1:
            pass

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
        if isinstance(structure, s.Fortress):
            if self.board[self.height - y][x - 1]["alive"] == 0:
                self.board[self.height - y][x - 1]["alive"] = structure

        elif (isinstance(structure, s.GunTurret) or 
              isinstance(structure, s.SubspaceBeacon)):
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

    def cast_spell(self, x, y, spell):
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

        elif isinstance(spell, sp.AlignTech):
            self.align_tech(spell.level)

        elif isinstance(spell, sp.AlignLife):
            self.align_life(spell.level)


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