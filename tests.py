import random
import board as b
import creatures as c

drone = c.Creature(name="Drone", probability=0.9, strength=1, defense=3,
                 speed=4, resist=4, alignment="T")

psi_lord = c.RangedCreature(name="Psi Lord", probability=0.7, strength=3,
                          defense=3, speed=2, resist=7, alignment="N",
                          range=2, rstr=1)

floating_eye = c.FlyingCreature(name="Floating Eye", probability=0.5, strength=4,
                               defense=3, speed=6, resist=3, alignment="L")

slime_beast = c.SlimyCreature(name="Slime Beast", probability=0.5, strength=4,
                               defense=3, speed=3, resist=5, alignment="L")

jeep = c.Mount(name="Jeep", probability=0.9, strength=2,
                               defense=2, speed=4, resist=4, alignment="T")

hovership = c.FlyingMount(name="Hovership", probability=0.6,
                        strength=2, defense=5, speed=5,
                        resist=4, alignment='T')

flying_slime = c.FlyingSlimyCreature(name="Flying Slime", probability=0.4,
                                   strength=5, defense=4, speed=4,
                                   resist=6, alignment='L')

hover_tank = c.FlyingRangedMount(name="Hover Tank", probability=0.4,
                                  strength=5, defense=6, speed=4,
                                  resist=4, alignment='T', range=3, rstr=2)

print drone
print psi_lord
print floating_eye
print slime_beast
print jeep
print hovership
print flying_slime
print hover_tank

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