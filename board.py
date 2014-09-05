from __future__ import print_function
import random
import creatures as c

class Gameboard(object):
    def __init__(self, width, height, number_of_players):
        self.width = width
        self.height = height
        self.number_of_players = number_of_players
        self.board = []
        for row in range(height):
            self.board.append([])
            for column in range(width):
                self.board[row].append(0)
        self.alignment = 0
        round_count = 1
        message = ""

    def printboard(self):
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
            for element in list_of_elements:
                try:
                    print ("{}".format(element.name[0]), end=' ')
                except:
                    print (" ".format(), end=' ')
            print ('|')
        print(' ', sep='', end='')
        print('-' * (self.width * 2), sep='')

    def spawn_commanders(self,):
        if number_of_players == 1:
            board[4][6] = commander

    def beam_creature(self, x, y, creature):
        r = random.randint(1, 10) / 10.0
        if creature.probability >= r:
            self.message = "SUCCESS"
            self.board[self.height - y][x - 1] = creature
        else:
            self.message = "FAILURE"

    def holo_creature(self, x, y, creature):
        self.message = "SUCCESS"
        self.board[self.height - y][x - 1] = creature
        creature.holograph = True

    # def beam_structure(self, x, y, structure):

    def kill_creature(self, x, y):
        self.board[self.height - y][x - 1] = 0

    def kill_structure(self, x, y, structure):
        self.board[self.height - y][x - 1] = 0

    def kill_commander(self, x, y, commander):
        self.board[self.height - y][x - 1] = 0

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