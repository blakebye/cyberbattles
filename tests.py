import random
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