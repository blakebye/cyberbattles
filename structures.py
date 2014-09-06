class Structure(object):
    def __init__(self):
        pass

class Fortress(Structure):
    def __init__(self):
        self.name = "Fortress"
        self.probability = 0.6
        self.alignment = 1

class GunTurret(Structure):
    def __init__(self):
        self.name = "Gun Turret"
        self.probability = 0.5
        self.alignment = 1

class SubspaceBeacon(Structure):
    def __init__(self):
        self.name = "SubspaceBeacon"
        self.probability = 0.9
        self.alignment = 1

class ForceField(Structure):
    def __init__(self):
        self.name = "Force Field"
        self.probability = 0.9
        self.alignment = 1