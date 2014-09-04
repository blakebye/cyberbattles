# POTENTIALLY ADD THE COMMANDER IN CONTROL TO THE CREATURE CLASS?

class Creature(object):
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        self.name = name
        self.probability = probability
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.resist = resist
        self.alignment = alignment
        self.range = 0
        self.rstr = 0
        self.cast_range = 1
        self.flight = False
        self.slimy = False
        self.mount = False

    def __repr__(self):
        return ("name: {}\nprobability: {}\n"
                "str: {}\ndef: {}\nspd: {}\n"
                "res: {}\nalign: {}\n").format(self.name, self.probability,
                                              self.strength, self.defense,
                                              self.speed, self.resist,
                                              self.alignment)

class RangedCreature(Creature):
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment, range, rstr):
        super(RangedCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.range = range
        self.rstr = rstr

    def __repr__(self):
        return (super(RangedCreature, self).__repr__() +
        "range: {}\nrange str: {}\n".format(self.range, self.rstr))

class FlyingCreature(Creature):
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        super(FlyingCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingCreature, self).__repr__() +
        "Flight: {}\n").format(self.flight)


class SlimyCreature(Creature):
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        super(SlimyCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.slimy = True

    def __repr__(self):
        return (super(SlimyCreature, self).__repr__() +
        "Slime: {}\n").format(self.slimy)

class Mount(Creature):
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        super(Mount, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.mount = True
        self.occupied = False

    def __repr__(self):
        return (super(Mount, self).__repr__() +
        "Mount: {}\nOccupied: {}\n").format(self.mount, self.occupied)

class FlyingMount(Mount, FlyingCreature):
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        super(FlyingMount, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingMount, self).__repr__())

class FlyingSlimyCreature(SlimyCreature, FlyingCreature):
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        super(FlyingSlimyCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingSlimyCreature, self).__repr__())

class FlyingRangedMount(Mount, FlyingCreature, RangedCreature):
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment, range, rstr):
        super(RangedCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.flight = True
        self.range = range
        self.rstr = rstr
        self.mount = True
        self.occupied = False

    def __repr__(self):
        return (super(FlyingRangedMount, self).__repr__())

# drone = Creature(name="Drone", probability=0.9, strength=1, defense=3,
#                  speed=4, resist=4, alignment="T")

# psi_lord = RangedCreature(name="Psi Lord", probability=0.7, strength=3,
#                           defense=3, speed=2, resist=7, alignment="N",
#                           range=2, rstr=1)

# floating_eye = FlyingCreature(name="Floating Eye", probability=0.5, strength=4,
#                                defense=3, speed=6, resist=3, alignment="L")

# slime_beast = SlimyCreature(name="Slime Beast", probability=0.5, strength=4,
#                                defense=3, speed=3, resist=5, alignment="L")

# jeep = Mount(name="Jeep", probability=0.9, strength=2,
#                                defense=2, speed=4, resist=4, alignment="T")

# hovership = FlyingMount(name="Hovership", probability=0.6,
#                         strength=2, defense=5, speed=5,
#                         resist=4, alignment='T')

# flying_slime = FlyingSlimyCreature(name="Flying Slime", probability=0.4,
#                                    strength=5, defense=4, speed=4,
#                                    resist=6, alignment='L')

# hover_tank = FlyingRangedMount(name="Hover Tank", probability=0.4,
#                                   strength=5, defense=6, speed=4,
#                                   resist=4, alignment='T', range=3, rstr=2)

# print drone
# print psi_lord
# print floating_eye
# print slime_beast
# print jeep
# print hovership
# print flying_slime
# print hover_tank