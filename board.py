import random
import creatures as c

class Gameboard(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        for row in range(height):
            self.board.append([])
            for column in range(width):
                self.board[row].append(0)
        self.alignment = 0
        turn_count = 1
        message = ""

    def printboard(self):
        for row in range(len(self.board)):
            list_of_elements = []
            for element in self.board[row]:
                if isinstance(element, c.Creature):
                    list_of_elements.append(element)
                else:
                    list_of_elements.append(0)
            for element in list_of_elements:
                try:
                    print "{}".format(element.name[0]) ,
                except:
                    print "0".format() ,
            print

    def beam_creature(self, x, y, creature):
        r = random.randint(1, 10) / 10.0
        if creature.probability >= r:
            self.message = "SUCCESS"
            self.board[self.height - y][x - 1] = creature

    def holo_creature(self, x, y, creature):
        self.message = "SUCCESS"
        self.board[self.height - y][x - 1] = creature
        creature.holograph = True

    def kill_creature(self, x, y):
        self.board[self.height - y][x - 1] = 0

    # def beam_structure(self, x, y, structure):

    # def kill_creature(self, x, y, creature):

    # def kill_structure(self, x, y, structure):

    # def kill_commander(self, x, y, commander):

    # def align_life(self):
    #     self.alignment -= 1

    # def align_tech(self):
    #     self.alignment += 1

    def next_turn(self):
        if self.turn_count >= 35:
            message = "Game Over, result is DRAW"
        else:
            self.turn_count += 1

gameboard = Gameboard(14, 10)
hover_tank = c.FlyingRangedMount(name="Hover Tank", probability=0.4,
                                  strength=5, defense=6, speed=4,
                                  resist=4, alignment='T', range=3, rstr=2)

flying_slime = c.FlyingSlimyCreature(name="Flying Slime", probability=0.4,
                                   strength=5, defense=4, speed=4,
                                   resist=6, alignment='L')