import random
import creatures

class AlienHatchling(creatures.Creature):
    def __init__(self):
        super(AlienHatchling, self).__init__("Alien Hatchling", 
                                             0.9, 2, 3, 1, 0, -2)

class Probe(creatures.FlyingCreature):
    def __init__(self):
        super(Probe, self).__init__("Probe", 0.9, 1, 1, 4, 2, 1)

class Droid(creatures.Creature):
    def __init__(self):
        super(Droid, self).__init__("Droid", 0.8, 3, 2, 1, 3, 1)

class SlimeBlob(creatures.SlimyCreature):
    def __init__(self):
        super(SlimeBlob, self).__init__("Slime Blob", 0.7, 3, 2, 1, 3, -1)

class LaserRobot(creatures.RangedCreature):
    def __init__(self):
        super(LaserRobot, self).__init__("Laser Robot", 0.6, 
                                         5, 1, 2, 4, 2, 5, 4)

class FloatingEye(creatures.FlyingCreature):
    def __init__(self):
        super(FloatingEye, self).__init__("Floating Eye", 0.5, 4, 3, 6, 3, -1)

class FaceGrabber(creatures.Creature):
    def __init__(self):
        super(FaceGrabber, self).__init__("Face Grabber", 0.8, 2, 2, 3, 4, -2)

class Jeep(creatures.Mount):
    def __init__(self):
        super(Jeep, self).__init__("Jeep", 0.9, 2, 2, 4, 4, 1)

class SlimeWarrior(creatures.SlimyCreature):
    def __init__(self):
        super(SlimeWarrior, self).__init__("Slime Warrior", 0.6, 4, 2, 2, 4, -1)

class Drone(creatures.Creature):
    def __init__(self):
        super(Drone, self).__init__("Drone", 0.9, 1, 3, 4, 4, 1)

class SentryRobot(creatures.Creature):
    def __init__(self):
        super(SentryRobot, self).__init__("Sentry Robot", 0.7, 3, 2, 2, 5, 1)

class Alien(creatures.Creature):
    def __init__(self):
        super(Alien, self).__init__("Alien", 0.7, 3, 3, 2, 5, 2)

class FireFox(creatures.Mount):
    def __init__(self):
        super(FireFox, self).__init__("Fire Fox", 0.7, 1, 3, 3, 5, -1)

class SlimeBeast(creatures.SlimyCreature):
    def __init__(self):
        super(SlimeBeast, self).__init__("Slime Beast", 0.5, 4, 3, 3, 5, -2)

class Hovership(creatures.FlyingMount):
    def __init__(self):
        super(Hovership, self).__init__("Hovership", 0.6, 2, 5, 5, 4, 2)

class MutantMount(creatures.Mount):
    def __init__(self):
        super(MutantMount, self).__init__("Mutant Mount", 0.6, 3, 4, 5, 5, -2)

class Cyborg(creatures.Creature):
    def __init__(self):
        super(Cyborg, self).__init__("Cyborg", 0.5, 6, 6, 2, 4, 0)

class HoverTank(creatures.FlyingRangedMount):
    def __init__(self):
        super(HoverTank, self).__init__("Hover Tank", 0.4, 5, 6, 4, 4, 2, 3, 2)

class MiningDroid(creatures.RangedCreature):
    def __init__(self):
        super(MiningDroid, self).__init__("Mining Droid", 0.6, 
                                          5, 6, 1, 4, 1, 2, 2)

class Tank(creatures.RangedMount):
    def __init__(self):
        super(Tank, self).__init__("Tank", 0.5, 5, 6, 2, 4, 2, 4, 2)

class FlyingSlime(creatures.FlyingSlimyCreature):
    def __init__(self):
        super(FlyingSlime, self).__init__("Flying Slime", 0.4, 5, 4, 4, 6, -2)

class PsiLord(creatures.RangedCreature):
    def __init__(self):
        super(PsiLord, self).__init__("Psi-Lord", 0.7, 3, 3, 2, 7, 0, 2, 1)

class PsiWarrior(creatures.Creature):
    def __init__(self):
        super(PsiWarrior, self).__init__("Psi-Warrior", 0.8, 2, 3, 1, 7, 0)

class AcidSpitter(creatures.RangedCreature):
    def __init__(self):
        super(AcidSpitter, self).__init__("Acid Spitter", 0.6,
                                          5, 6, 1, 5, -1, 3, 3)

class Mutant(creatures.Creature):
    def __init__(self):
        super(Mutant, self).__init__("Mutant", 0.6, 6, 6, 1, 5, -1)

class AlienQueen(creatures.RangedCreature):
    def __init__(self):
        super(AlienQueen, self).__init__("Alien Queen", 0.1,
                                         8, 8, 4, 5, -2, 3, 4)

class MechWarrior(creatures.RangedCreature):
    def __init__(self):
        super(MechWarrior, self).__init__("Mech Warrior", 0.1,
                                         9, 9, 3, 5, 2, 3, 4)

class Tentacle(creatures.Creature):
    def __init__(self):
        super(Tentacle, self).__init__("Tentacle", 0.5, 8, 8, 1, 6, -1)

class Predator(creatures.Creature):
    def __init__(self):
        super(Predator, self).__init__("Predator", 0.2, 9, 7, 5, 8, -2)

class Spideroid(creatures.Creature):
    def __init__(self):
        super(Spideroid, self).__init__("Spideroid", 0.2, 8, 8, 6, 8, 2)

class Structure(object):
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0

class Fortress(Structure):
    def __init__(self):
        self.name = "Fortress"
        self.probability = 0.6

class GunTurret(Structure):
    def __init__(self):
        self.name = "Gun Turret"
        self.probability = 0.5

class SubspaceBeacon(Structure):
    def __init__(self):
        self.name = "Subspace Beacon"
        self.probability = 0.9

class ForceField(Structure):
    def __init__(self):
        self.name = "Force Field"
        self.probability = 0.9

class Spell(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.commander = 0

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
        self.alignment = 0
        self.cast_range = 6

class Disintegrate(Spell):
    def __init__(self):
        self.name = "Disintegrate"
        self.probability = 1.00
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
    def __init__(self):
        self.name = "Teleport"
        self.probability = 0.7
        self.alignment = 0
        self.cast_range = 7

class Fire(Spell):
    def __init__(self):
        self.name = "Fire"
        self.probability = 0.9
        self.alignment = 0
        self.cast_range = 6

class AlienGoo(Spell):
    def __init__(self):
        self.name = "Alien Goo"
        self.probability = 0.9
        self.alignment = 1
        self.cast_range = 6

class Upgrade(object):
    def __init__(self):
        # all upgrades are tech except for symbiont
        self.alignment = 1
        self.commander = 0

class TechnologyOne(Upgrade):
    def __init__(self):
        self.name = "Technology 1"
        self.probability = 0.8
        self.alignment = 1

class TechnologyTwo(Upgrade):
    def __init__(self):
        self.name = "Technology 2"
        self.probability = 0.6
        self.alignment = 2

class LifeforceOne(Upgrade):
    def __init__(self):
        self.name = "Lifeforce 1"
        self.probability = 0.8
        self.alignment = -1

class LifeforceTwo(Upgrade):
    def __init__(self):
        self.name = "Lifeforce 2"
        self.probability = 0.6
        self.alignment = -2

class Blaster(Upgrade):
    def __init__(self):
        self.name = "Blaster"
        self.probability = 0.5

class ForceShield(Upgrade):
    def __init__(self):
        self.name = "Force Shield"
        self.probability = 0.6

class ForceArmor(Upgrade):
    def __init__(self):
        self.name = "Force Armor"
        self.probability = 0.4

class Jetpack(Upgrade):
    def __init__(self):
        self.name = "Jetpack"
        self.probability = 0.5

class LightSabre(Upgrade):
    def __init__(self):
        self.name = "Light-Sabre"
        self.probability = 0.6

class Symbiont(Upgrade):
    def __init__(self):
        self.name = "Symbiont"
        self.probability = 0.5
        self.alignment = -1

def return_hand():
    all_cards = [AlienHatchling(), Probe(), Droid(), SlimeBlob(), LaserRobot(),
                 FloatingEye(), FaceGrabber(), Jeep(), SlimeWarrior(), Drone(),
                 SentryRobot(), Alien(), FireFox(), SlimeBeast(), Hovership(),
                 MutantMount(), Cyborg(), HoverTank(), MiningDroid(), Tank(),
                 FlyingSlime(), PsiLord(), PsiWarrior(), AcidSpitter(),
                 Mutant(), AlienQueen(), MechWarrior(), Tentacle(), Predator(),
                 Spideroid(), Fortress(), GunTurret(), SubspaceBeacon(),
                 ForceField(), Mutate(), Hypnotize(), Resurrect(), Disrupt(),
                 Disintegrate(), EMP(), Virus(), Teleport(), Fire(), AlienGoo(),
                 TechnologyOne(), TechnologyTwo(), LifeforceOne(), 
                 LifeforceTwo(), Blaster(), ForceShield(), ForceArmor(),
                 Jetpack(), LightSabre(), Symbiont()]

    hand = [HoloDetect(), random.sample(all_cards, 17)]
    return hand