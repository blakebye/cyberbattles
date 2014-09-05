import random
import creatures as c
import board as b

gameboard = b.Gameboard(15, 10, 1)

mech_warrior = c.RangedCreature(name="Mech Warrior", probability=0.1,
                                strength=9, defense=9, speed=3,
                                resist=5, alignment='T', range=3, rstr=4)
print "MECH WARRIOR CHANCE TO SPAWN ON EVERY SQUARE"

for i in range(10):
    for j in range(15):
        gameboard.beam_creature(j + 1, i + 1, mech_warrior)
gameboard.printboard()

print "LEFT HALF OF BOARD IS KILLED, STILL NEED CORPSES"
for i in range(10):
    for j in range(7):
        gameboard.kill_creature(j + 1, i + 1)
gameboard.printboard()