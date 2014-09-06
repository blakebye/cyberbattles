"""
This module gives a way to generate all of the creatures that fight
in CyberBattles. Some creatures can attack from range in addition to melee,
some creatures move via flight and aren't obstructed, and some creatures are
slimy and can't be melee attacked by non-slime creatures. Some creatures
double as a "mount", which will hold your commander rendering him
unattackable until the mount is dead, and potentially give him 
extra speed or flight in some cases.
"""
class Creature(object):
    """This is the basic melee creature"""
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
        self.holograph = False

    def __repr__(self):
        return ("{}\nname: {}\nprobability: {}\n"
                "str: {}\ndef: {}\nspd: {}\n"
                "res: {}\nalign: {}\n").format(type(self), self.name,
                                               self.probability,
                                               self.strength, self.defense,
                                               self.speed, self.resist,
                                               self.alignment)

class Commander(Creature):
    """This creature is a commander."""
    def __init__(self):
        self.strength = 5
        self.defense = 5
        self.speed = 1
        self.resist = 7
        self.flight = False
        self.on_mount = False

    def __repr__(self):
        return ("This is a commander.\n"
                "Flight = {}\n"
                "Mounted = {}".format(self.flight, self.on_mount))

class RangedCreature(Creature):
    """This creature can attack from range and melee"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment, range, rstr):
        # define a rangedcreature by defining a creature and then
        # giving this creature its range and strength
        super(RangedCreature, self).__init__(name, probability, strength,
                                             defense, speed, resist, alignment)
        self.range = range
        self.rstr = rstr

    def __repr__(self):
        return (super(RangedCreature, self).__repr__() +
        "range: {}\nrange str: {}\n".format(self.range, self.rstr))

class FlyingCreature(Creature):
    """This creature can move unobstructed by other creatures/structures"""
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        # define a flyingcreature by definint a creature and then
        # giving this creature the property of flight
        super(FlyingCreature, self).__init__(name, probability, strength,
                                            defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingCreature, self).__repr__() +
        "Flight: {}\n").format(self.flight)


class SlimyCreature(Creature):
    """This creature can't be melee attacked by non-slime creatures"""
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        # define a slimycreature by defining a creature and then
        # giving this creature the property of slime
        super(SlimyCreature, self).__init__(name, probability, strength,
                                            defense, speed, resist, alignment)
        self.slimy = True

    def __repr__(self):
        return (super(SlimyCreature, self).__repr__() +
        "Slime: {}\n").format(self.slimy)

class Mount(Creature):
    """This creature can hold your commander"""
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        # define a mount as a creature and then give it
        # the properties of mount and unoccupied
        super(Mount, self).__init__(name, probability, strength,
                                    defense, speed, resist, alignment)
        self.mount = True
        self.occupied = False

    def __repr__(self):
        return (super(Mount, self).__repr__() +
        "Mount: {}\nOccupied: {}\n").format(self.mount, self.occupied)

class FlyingMount(Mount, FlyingCreature):
    """This creature can hold your commander and fly"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        # define a flying mount by defining a mount and then
        # giving it the property of flight
        super(FlyingMount, self).__init__(name, probability, strength,
                                          defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingMount, self).__repr__())

class FlyingSlimyCreature(SlimyCreature, FlyingCreature):
    """This creature is slimy and flying"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        # define a flying slimy creature by first defining a slimy
        # creature and then giving it the property of flight
        super(FlyingSlimyCreature, self).__init__(name, probability, strength,
                                           defense, speed, resist, alignment)
        self.flight = True

    def __repr__(self):
        return (super(FlyingSlimyCreature, self).__repr__())

class FlyingRangedMount(Mount, FlyingCreature, RangedCreature):
    """This creature can hold your commander, fly, and has a ranged attack"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment, range, rstr):
        # define a flying ranged mount by first defining it as a creature
        # and then giving it the properties of flight, range, and mount
        super(RangedCreature, self).__init__(name, probability, strength,
                                           defense, speed, resist, alignment)
        self.flight = True
        self.range = range
        self.rstr = rstr
        self.mount = True
        self.occupied = False

    def __repr__(self):
            return (super(FlyingRangedMount, self).__repr__())
