class Structure(object):
    def __init__(self):
        pass

class Fortress(Structure):
    def __init__(self):
        self.name = "Fortress"
        self.probability = 0.6
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0

class GunTurret(Structure):
    def __init__(self):
        self.name = "Gun Turret"
        self.probability = 0.5
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0

class SubspaceBeacon(Structure):
    def __init__(self):
        self.name = "Subspace Beacon"
        self.probability = 0.9
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0

class ForceField(Structure):
    def __init__(self):
        self.name = "Force Field"
        self.probability = 0.9
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0