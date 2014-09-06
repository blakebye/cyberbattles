class Structure(object):
    def __init__(self):
        pass

class Fortress(Structure):
    def __init__(self):
        self.name = "Fortress"
        self.probability = 0.6
        self.alignment = 'T'

class GunTurret(Structure):
    def __init__(self):
        self.name = "Gun Turret"
        self.probability = 0.5
        self.alignment = 'T'

class SubspaceBeacon(Structure):
    def __init__(self):
        self.name = "SubspaceBeacon"
        self.probability = 0.9
        self.alignment = 'T'

class ForceField(Structure):
    def __init__(self):
        self.name = "Force Field"
        self.probability = 0.9
        self.alignment = 'T'