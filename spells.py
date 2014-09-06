class Spell(object):
    def __init__(self):
        pass

class HoloDetect(Spell):
    def __init__(self):
        self.name = "HoloDetect"
        self.probability = 1.00
        self.alignment = 0
        self.cast_range = 20

class Mutate(Spell):
    def __init__(self):
        self.name = "Mutate"
        self.probability = 0.7
        self.alignment = -1
        self.cast_range = 4

class Hypnotize(Spell):
    def __init__(self):
        self.name = "Hypnotize"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE
        self.alignment = 0
        self.cast_range = 7

class Resurrect(Spell):
    def __init__(self):
        self.name = "Resurrect"
        self.probability = 0.6
        self.alignment = -1
        self.cast_range = 4

class Disrupt(Spell):
    def __init__(self):
        self.name = "Disrupt"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE AND DEFENSE
        self.alignment = 0
        self.cast_range = 6

class Disintegrate(Spell):
    def __init__(self):
        self.name = "Disintegrate"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE AND DEFENSE
        self.alignment = 0
        self.cast_range = 4

class EMP(Spell):
    def __init__(self):
        self.name = "EMP"
        self.probability = 0.5
        self.alignment = 1
        self.cast_range = 20

class Virus(Spell):
    def __init__(self):
        self.name = "Virus"
        self.probability = 0.5
        self.alignment = -1
        self.cast_range = 20

class Teleport(Spell):
    def __init__(self, dest_x, dest_y):
        self.name = "Teleport"
        self.probability = 0.7
        self.alignment = 0
        self.cast_range = 7
        self.dest_x = dest_x
        self.dest_y = dest_y

class Align(Spell):
    def __init__(self, direction, level):
        self.name = "%s %i" % (direction, level)
        self.direction = direction
        self.level = level
        self.probability = 1.0 - level * .2
        self.alignment = -1