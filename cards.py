import random

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
        self.x = 0
        self.y = 0
        self.commander = 0

    def movable_squares(self):
        movable = []

class Commander(Creature):
    """This creature is a commander."""
    def __init__(self):
        self.name = "Commander"
        self.strength = 5
        self.defense = 5
        self.speed = 1
        self.resist = 7
        self.range = 1
        self.flight = False
        self.on_mount = False
        self.gameboard = 0
        self.x = 0
        self.y = 0
        self.hand = self.create_hand()
        self.creatures = []

    def create_hand(self):
        all_cards = [AlienHatchling(), Probe(), Droid(), SlimeBlob(), 
                     LaserRobot(), FloatingEye(), FaceGrabber(), Jeep(), 
                     SlimeWarrior(), Drone(), SentryRobot(), Alien(), FireFox(),
                     SlimeBeast(), Hovership(), MutantMount(), Cyborg(), 
                     HoverTank(), MiningDroid(), Tank(), FlyingSlime(), 
                     PsiLord(), PsiWarrior(), AcidSpitter(), Mutant(), 
                     AlienQueen(), MechWarrior(), Tentacle(), Predator(),
                     Spideroid(), Fortress(), GunTurret(), SubspaceBeacon(),
                     ForceField(), Mutate(), Hypnotize(), Resurrect(), 
                     Disrupt(), Disintegrate(), EMP(), Virus(), Teleport(), 
                     Fire(), AlienGoo(), TechnologyOne(), TechnologyTwo(), 
                     LifeforceOne(), LifeforceTwo(), Blaster(), ForceShield(), 
                     ForceArmor(), Jetpack(), LightSabre(), Symbiont()]

        # this will generate a hand full of 17 random cards + holodetect
        hand = random.sample(all_cards, 17)
        hand.insert(0, HoloDetect())

        # this ensures each card is assigned the proper commander.
        for card in hand:
            card.commander = self
        return hand

    def play_card(self, card):
        if isinstance(card, Creature):
            self.hand[self.hand.index(card)] = 0
            # TODO - CHOICE BETWEEN BEAM AND HOLO

        elif isinstance(card, Structure):
            # TODO - MAKE SURE STRUCTURES HAVE TO PASS PROBABILITY
            self.hand[self.hand.index(card)] = 0

            # let board alignment influence structure probability
            if self.gameboard.alignment > 0:
                success = abs(self.gameboard.alignment / 10.0 +
                              card.probability)
            else:
                success = card.probability

            r = random.randint(1, 10) / 10
            if success >= r:

                if isinstance(card, Fortress):
                    # TODO - FORTRESS NEEDS A TARGETTING SUBSKILL
                    pass

                elif isinstance(card, ForceField):
                    for i, j in ((self.x - 2, self.y + 1), 
                                 (self.x - 2, self.y + 2), 
                                 (self.x - 1, self.y + 2), 
                                 (self.x + 2, self.y + 1),
                                 (self.x + 2, self.y + 2), 
                                 (self.x + 1, self.y + 2),
                                 (self.x - 2, self.y - 1), 
                                 (self.x - 2, self.y - 2), 
                                 (self.x - 1, self.y - 2), 
                                 (self.x + 2, self.y - 1),
                                 (self.x + 2, self.y - 2), 
                                 (self.x + 1, self.y - 2)):
                        if (j > 0 and i > 0 and j <= self.gameboard.height and 
                            i <= self.gameboard.width):
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[self.gameboard.height - j]\
                                [i - 1]["alive"] = card

                elif isinstance(card, GunTurret):
                    for i, j in ((self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 2), 
                                 (self.x, self.y - 2), (self.x - 2, self.y + 2), 
                                 (self.x + 2, self.y + 2), (self.x - 2, self.y - 2), 
                                 (self.x + 2, self.y - 2)):
                        if (j > 0 and i > 0 and j <= self.gameboard.height and 
                            i <= self.gameboard.width):
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[self.gameboard.height - j]\
                                [i - 1]["alive"] = GunTurret()

                elif isinstance(card, SubspaceBeacon):
                    for i, j in ((self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 2), 
                                 (self.x, self.y - 2), (self.x - 2, self.y + 2), 
                                 (self.x + 2, self.y + 2), (self.x - 2, self.y - 2), 
                                 (self.x + 2, self.y - 2)):
                        if (j > 0 and i > 0 and j <= self.gameboard.height and 
                            i <= self.gameboard.width):
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[self.gameboard.height - j]\
                                [i - 1]["alive"] = SubspaceBeacon()

            else:
                # structure failed
                pass

        elif isinstance(card, Spell):
            if isinstance(card, HoloDetect):
                # TODO - FLYING SPELL, CHECK FOR CASTABLE SQUARES
                pass

            elif isinstance(card, Virus) or isinstance(card, EMP):
                self.hand[self.hand.index(card)] = 0
                # TODO - NEITHER OF THESE SPELLS REQUIRE LINE OF SIGHT

            else:
                self.hand[self.hand.index(card)] = 0
                # TODO - ALL THESE SPELLS REQUIRE LINE OF SIGHT

        elif isinstance(card, Upgrade):
            # remove card from hand
            self.hand[self.hand.index(card)] = 0

            # let board alignment influence upgrade probability
            if self.gameboard.alignment * card.alignment > 0:
                success = abs(self.gameboard.alignment / 10.0 +
                              card.probability)
            else:
                success = card.probability

            r = random.randint(1, 10) / 10
            if success >= r:
                if isinstance(card, Symbiont):
                    self.strength = max(self.strength, 6)
                    self.defense = max(self.defense, 6)
                    self.speed = max(self.speed, 2)
                    self.resist = max(self.resist, 8)

                elif isinstance(card, ForceShield):
                    self.defense = max(self.defense, 7)

                elif isinstance(card, ForceArmor):
                    self.defense = max(self.defense, 8)

                elif isinstance(card, Blaster):
                    self.range = max(self.range, 3)

                elif isinstance(card, LightSabre):
                    self.strength = max(self.strength, 7)

                elif isinstance(card, Jetpack):
                    self.speed = max(self.speed, 3)
                    self.flight = True

                elif isinstance(card, TechnologyOne):
                    self.gameboard.alignment += 1

                elif isinstance(card, TechnologyTwo):
                    self.gameboard.alignment += 2

                elif isinstance(card, LifeforceOne):
                    self.gameboard.alignment -= 1

                elif isinstance(card, LifeforceOne):
                    self.gameboard.alignment -= 2

            else:
                # upgrade failed
                pass



    def add_creature(creature):
        self.creatures.append(creature)

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

class FlyingCreature(Creature):
    """This creature can move unobstructed by other creatures/structures"""
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        # define a flyingcreature by definint a creature and then
        # giving this creature the property of flight
        super(FlyingCreature, self).__init__(name, probability, strength,
                                            defense, speed, resist, alignment)
        self.flight = True

class SlimyCreature(Creature):
    """This creature can't be melee attacked by non-slime creatures"""
    def __init__(self, name, probability, strength,
                 defense, speed, resist, alignment):
        # define a slimycreature by defining a creature and then
        # giving this creature the property of slime
        super(SlimyCreature, self).__init__(name, probability, strength,
                                            defense, speed, resist, alignment)
        self.slimy = True

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

class FlyingMount(Mount, FlyingCreature):
    """This creature can hold your commander and fly"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        # define a flying mount by defining a mount and then
        # giving it the property of flight
        super(FlyingMount, self).__init__(name, probability, strength,
                                          defense, speed, resist, alignment)
        self.flight = True

class RangedMount(Mount, RangedCreature):
    """This creature can hold your commander and fly"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment, range, rstr):
        # define a ranged mount by defining a mount and then
        # giving it the property of range
        super(RangedCreature, self).__init__(name, probability, strength, 
                                             defense, speed, resist, alignment)
        self.range = range
        self.rstr = rstr
        self.mount = True
        self.occupied = False

class FlyingSlimyCreature(SlimyCreature, FlyingCreature):
    """This creature is slimy and flying"""
    def __init__(self, name, probability, strength, defense,
                 speed, resist, alignment):
        # define a flying slimy creature by first defining a slimy
        # creature and then giving it the property of flight
        super(FlyingSlimyCreature, self).__init__(name, probability, strength,
                                           defense, speed, resist, alignment)
        self.flight = True

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

class AlienHatchling(Creature):
    def __init__(self):
        super(AlienHatchling, self).__init__("Alien Hatchling", 
                                             0.9, 2, 3, 1, 0, -2)

class Probe(FlyingCreature):
    def __init__(self):
        super(Probe, self).__init__("Probe", 0.9, 1, 1, 4, 2, 1)

class Droid(Creature):
    def __init__(self):
        super(Droid, self).__init__("Droid", 0.8, 3, 2, 1, 3, 1)

class SlimeBlob(SlimyCreature):
    def __init__(self):
        super(SlimeBlob, self).__init__("Slime Blob", 0.7, 3, 2, 1, 3, -1)

class LaserRobot(RangedCreature):
    def __init__(self):
        super(LaserRobot, self).__init__("Laser Robot", 0.6, 
                                         5, 1, 2, 4, 2, 5, 4)

class FloatingEye(FlyingCreature):
    def __init__(self):
        super(FloatingEye, self).__init__("Floating Eye", 0.5, 4, 3, 6, 3, -1)

class FaceGrabber(Creature):
    def __init__(self):
        super(FaceGrabber, self).__init__("Face Grabber", 0.8, 2, 2, 3, 4, -2)

class Jeep(Mount):
    def __init__(self):
        super(Jeep, self).__init__("Jeep", 0.9, 2, 2, 4, 4, 1)

class SlimeWarrior(SlimyCreature):
    def __init__(self):
        super(SlimeWarrior, self).__init__("Slime Warrior", 0.6, 4, 2, 2, 4, -1)

class Drone(Creature):
    def __init__(self):
        super(Drone, self).__init__("Drone", 0.9, 1, 3, 4, 4, 1)

class SentryRobot(Creature):
    def __init__(self):
        super(SentryRobot, self).__init__("Sentry Robot", 0.7, 3, 2, 2, 5, 1)

class Alien(Creature):
    def __init__(self):
        super(Alien, self).__init__("Alien", 0.7, 3, 3, 2, 5, 2)

class FireFox(Mount):
    def __init__(self):
        super(FireFox, self).__init__("Fire Fox", 0.7, 1, 3, 3, 5, -1)

class SlimeBeast(SlimyCreature):
    def __init__(self):
        super(SlimeBeast, self).__init__("Slime Beast", 0.5, 4, 3, 3, 5, -2)

class Hovership(FlyingMount):
    def __init__(self):
        super(Hovership, self).__init__("Hovership", 0.6, 2, 5, 5, 4, 2)

class MutantMount(Mount):
    def __init__(self):
        super(MutantMount, self).__init__("Mutant Mount", 0.6, 3, 4, 5, 5, -2)

class Cyborg(Creature):
    def __init__(self):
        super(Cyborg, self).__init__("Cyborg", 0.5, 6, 6, 2, 4, 0)

class HoverTank(FlyingRangedMount):
    def __init__(self):
        super(HoverTank, self).__init__("Hover Tank", 0.4, 5, 6, 4, 4, 2, 3, 2)

class MiningDroid(RangedCreature):
    def __init__(self):
        super(MiningDroid, self).__init__("Mining Droid", 0.6, 
                                          5, 6, 1, 4, 1, 2, 2)

class Tank(RangedMount):
    def __init__(self):
        super(Tank, self).__init__("Tank", 0.5, 5, 6, 2, 4, 2, 4, 2)

class FlyingSlime(FlyingSlimyCreature):
    def __init__(self):
        super(FlyingSlime, self).__init__("Flying Slime", 0.4, 5, 4, 4, 6, -2)

class PsiLord(RangedCreature):
    def __init__(self):
        super(PsiLord, self).__init__("Psi-Lord", 0.7, 3, 3, 2, 7, 0, 2, 1)

class PsiWarrior(Creature):
    def __init__(self):
        super(PsiWarrior, self).__init__("Psi-Warrior", 0.8, 2, 3, 1, 7, 0)

class AcidSpitter(RangedCreature):
    def __init__(self):
        super(AcidSpitter, self).__init__("Acid Spitter", 0.6,
                                          5, 6, 1, 5, -1, 3, 3)

class Mutant(Creature):
    def __init__(self):
        super(Mutant, self).__init__("Mutant", 0.6, 6, 6, 1, 5, -1)

class AlienQueen(RangedCreature):
    def __init__(self):
        super(AlienQueen, self).__init__("Alien Queen", 0.1,
                                         8, 8, 4, 5, -2, 3, 4)

class MechWarrior(RangedCreature):
    def __init__(self):
        super(MechWarrior, self).__init__("Mech Warrior", 0.1,
                                         9, 9, 3, 5, 2, 3, 4)

class Tentacle(Creature):
    def __init__(self):
        super(Tentacle, self).__init__("Tentacle", 0.5, 8, 8, 1, 6, -1)

class Predator(Creature):
    def __init__(self):
        super(Predator, self).__init__("Predator", 0.2, 9, 7, 5, 8, -2)

class Spideroid(Creature):
    def __init__(self):
        super(Spideroid, self).__init__("Spideroid", 0.2, 8, 8, 6, 8, 2)

class Structure(object):
    def __init__(self):
        self.alignment = 1
        self.x = 0
        self.y = 0
        self.commander = 0

class Fortress(Structure):
    def __init__(self):
        super(Fortress, self).__init__()
        self.name = "Fortress"
        self.probability = 0.6

class GunTurret(Structure):
    def __init__(self):
        super(GunTurret, self).__init__()
        self.name = "Gun Turret"
        self.probability = 0.5

class SubspaceBeacon(Structure):
    def __init__(self):
        super(SubspaceBeacon, self).__init__()
        self.name = "Subspace Beacon"
        self.probability = 0.9

class ForceField(Structure):
    def __init__(self):
        super(ForceField, self).__init__()
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
        # upgrades don't need coordinates but it's easier this way
        self.x = 0
        self.y = 0

class TechnologyOne(Upgrade):
    def __init__(self):
        super(TechnologyOne, self).__init__()
        self.name = "Technology 1"
        self.probability = 0.8

class TechnologyTwo(Upgrade):
    def __init__(self):
        super(TechnologyTwo, self).__init__()
        self.name = "Technology 2"
        self.probability = 0.6
        self.alignment = 2

class LifeforceOne(Upgrade):
    def __init__(self):
        super(LifeforceOne, self).__init__()
        self.name = "Lifeforce 1"
        self.probability = 0.8
        self.alignment = -1

class LifeforceTwo(Upgrade):
    def __init__(self):
        super(LifeforceTwo, self).__init__()
        self.name = "Lifeforce 2"
        self.probability = 0.6
        self.alignment = -2

class Blaster(Upgrade):
    def __init__(self):
        super(Blaster, self).__init__()
        self.name = "Blaster"
        self.probability = 0.5

class ForceShield(Upgrade):
    def __init__(self):
        super(ForceShield, self).__init__()
        self.name = "Force Shield"
        self.probability = 0.6

class ForceArmor(Upgrade):
    def __init__(self):
        super(ForceArmor, self).__init__()
        self.name = "Force Armor"
        self.probability = 0.4

class Jetpack(Upgrade):
    def __init__(self):
        super(Jetpack, self).__init__()
        self.name = "Jetpack"
        self.probability = 0.5

class LightSabre(Upgrade):
    def __init__(self):
        super(LightSabre, self).__init__()
        self.name = "Light-Sabre"
        self.probability = 0.6

class Symbiont(Upgrade):
    def __init__(self):
        super(Symbiont, self).__init__()
        self.name = "Symbiont"
        self.probability = 0.5
        self.alignment = -1
