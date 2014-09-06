class Spell(object):
    def __init__(self):
        pass

class HoloDetect(Spell):
    def __init__(self):
        self.name = "HoloDetect"
        self.probability = 1.00
        self.alignment = 0

class Mutate(Spell):
    def __init__(self):
        self.name = "Mutate"
        self.probability = 0.7
        self.alignment = -1

class Hypnotize(Spell):
    def __init__(self):
        self.name = "Hypnotize"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE
        self.alignment = 0

class Resurrect(Spell):
    def __init__(self):
        self.name = "Resurrect"
        self.probability = 0.6
        self.alignment = -1

class Disrupt(Spell):
    def __init__(self):
        self.name = "Disrupt"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE AND DEFENSE
        self.alignment = 0

class Disintegrate(Spell):
    def __init__(self):
        self.name = "Disintegrate"
        self.probability = 1.00
        # DEPENDS ON RESISTANCE AND DEFENSE
        self.alignment = 0

class EMP(Spell):
    def __init__(self):
        self.name = "EMP"
        self.probability = 0.5
        self.alignment = 1

class Virus(Spell):
    def __init__(self):
        self.name = "Virus"
        self.probability = 0.5
        self.alignment = -1

class Teleport(Spell):
    def __init__(self):
        self.name = "Teleport"
        self.probability = 0.7
        self.alignment = 0

class AlignLife(Spell):
    def __init__(self, level):
        self.name = "Lifeforce %i" % level
        self.level = level
        self.probability = 1.0 - level * .2
        self.alignment = -1

class AlignTech(Spell):
    def __init__(self, level):
        self.name = "Technology %i" % level
        self.level = level
        self.probability = 1.0 - level * .2
        self.alignment = 1