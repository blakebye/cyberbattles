import random
import creatures as c
import board as b

gameboard = b.Gameboard(15, 10, 1)

mech_warrior = c.RangedCreature(name="Mech Warrior", probability=0.1,
                                strength=9, defense=9, speed=3,
                                resist=5, alignment='T', range=3, rstr=4)

predator = c.Creature(name="Predator", probability=0.2,
                                strength=9, defense=7, speed=5,
                                resist=8, alignment='L')

print "Hologram a Predator on half the squares, randomly"

for i in range(10):
    for j in range(0, 15):
        if random.randint(1, 10) > 5:
            gameboard.holo_creature(j + 1, i + 1, predator)

gameboard.print_board()

print "Try to beam down a Mech Warrior on every square"

for i in range(10):
    for j in range(0, 15):
        gameboard.beam_creature(j + 1, i + 1, mech_warrior)

gameboard.print_board()

print "Kill the entire board, leaving behind corpses of only beamed down units"

for i in range(10):
    for j in range(15):
        if gameboard.check_living_creature(j + 1, i + 1) != 0:
            gameboard.kill_creature(j + 1, i + 1)

gameboard.print_board()