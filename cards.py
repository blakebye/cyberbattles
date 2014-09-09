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
        self.gameboard = 0
        self.x = 0
        self.y = 0
        self.commander = 0
        self.movement = speed
        self.moved = False

    def sees(self, x1, y1):
        """
        This function is Bresenham's line creation algorithm. It takes two
        end-points of a line on a grid and determines which points to fill in
        between the endpoints to make the best-fitting line. The points returned
        can be checked for occupants to determine sight.
        """

        x0, y0 = (self.x, self.y)
        # to do the integer algorithm, we need a function(x) we can't have
        # more than one value per x result, so the line can't be steep
        steep = abs(y1 - y0) > abs(x1 - x0)
        # we'll fix this by reflecting the line along y = x, the 45 degree
        # angle line, and then we'll make sure to fix the output later
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # for ease of the algoithm, we want to step one x value at a time,
        # so we make sure we're increasing from x0 and not decreasing
        backward = x0 > x1
        # we'll fix this by swapping the line's endpoints. this doesn't change
        # the line at all, only the direction we traverse it
        if backward:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # this will determine if we go up or down when the error has reached
        # a point at which our y value will change. it's the sign of the slope
        if y0 > y1:
            ystep = -1
        else:
            ystep = 1

        # this is the slope of the line. it is also the change in y for each
        # step we take in the x direction. it will be fractional
        dy = abs(float(y1 - y0) / float(x1 - x0))
        # this will be a value from 0 to 1. the only importance of this value
        # i whether it is closer to 0 or closer to 1, which will determine if
        # we will make a corresponding step in the y direction or not
        error = 0.0
        # this value will reflect its corresponding x for each point on the line
        y = y0
        # this will be a list of all points on the line
        line = []
        # visit each x point between the endpoints, not inclucing the last
        for x in range(x0, x1):
            # reflect the resulting point back across y = x
            # and add the resulting point to the line
            if steep:
                line.append((y, x))
            # add the resuling point to the line
            else:
                line.append((x, y))
            # increase the error term by the slope
            error += dy
            # if the error is closer to 1 than 0, then the spot where the line
            # crosses that x value is closer to the next value than the same
            # value, and we will bump the y to the next threshold
            if error >= 0.5:
                y += ystep
                error -= 1
        # our range didn't include the last point, and this pop will also
        # remove the first point. this will result in only evaluating the
        # squares between the creature and the point for obstructions
        line.pop(0)
        # let's assume at first that our source can see the destination
        seen = True
        # now check every point in the line for obstructions, and if there are
        # any, flag seen as false because our source can't see the destination
        for point in line:
            if self.occupant(point[0], point[1]) != 0:
                seen = False
        return seen

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
        self.x = 0
        self.y = 0
        self.hand = self.create_hand()
        self.creatures = [self]
        self.dead_creatures = []
        self.commander = self
        self.holograph = False
        self.moved = False
        self.action_card = BlankCard()
        self.holo_choice = ""

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

    def print_hand(self):
        cardnames = []
        for card in self.hand:
            cardnames.append(card.name)
        h = enumerate(cardnames, 1)
        for c in h:
            print c

    def rng(self):
        # let board alignment influence structure probability
        if self.gameboard.alignment * self.action_card.alignment > 0:
            success = (abs(self.gameboard.alignment) / 10.0 +
                          self.action_card.probability)
        else:
            success = self.action_card.probability

        r = random.randint(1, 10) / 10
        # passed the probability test
        if success >= r:
            return True
        else:
            return False

    def choose_card(self):
        self.gameboard.message = "%s's TURN" % self.name
        self.gameboard.print_board()
        self.print_hand()
        while isinstance(self.action_card, BlankCard):
            i = int(raw_input("Which number card would you like to play? ")) - 1
            self.action_card = self.hand[i]
        if isinstance(self.action_card, Creature):
            self.holo_choice = raw_input('Do you want to "Beam" or "Holo"? ')

    def target_card(self):
        self.gameboard.message = "%s's TURN" % self.name
        self.gameboard.print_board()
        # all upgrade cards need no targetting
        if isinstance(self.action_card, Upgrade):

            # remove card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

            if self.rng():
                if isinstance(self.action_card, Symbiont):
                    self.strength = max(self.strength, 6)
                    self.defense = max(self.defense, 6)
                    self.speed = max(self.speed, 2)
                    self.resist = max(self.resist, 8)

                elif isinstance(self.action_card, ForceShield):
                    self.defense = max(self.defense, 7)

                elif isinstance(self.action_card, ForceArmor):
                    self.defense = max(self.defense, 8)

                elif isinstance(self.action_card, Blaster):
                    self.range = max(self.range, 3)

                elif isinstance(self.action_card, LightSabre):
                    self.strength = max(self.strength, 7)

                elif isinstance(self.action_card, Jetpack):
                    self.speed = max(self.speed, 3)
                    self.flight = True

                elif isinstance(self.action_card, TechnologyOne):
                    self.gameboard.alignment += 1

                elif isinstance(self.action_card, TechnologyTwo):
                    self.gameboard.alignment += 2

                elif isinstance(self.action_card, LifeforceOne):
                    self.gameboard.alignment -= 1

                elif isinstance(self.action_card, LifeforceTwo):
                    self.gameboard.alignment -= 2

        # creatures have 1 range targetting
        elif isinstance(self.action_card, Creature):
            potential_squares = []
            for i, j in ((self.x - 1, self.y + 1), (self.x, self.y + 1),
                         (self.x + 1, self.y + 1), (self.x - 1, self.y),
                         (self.x + 1, self.y), (self.x - 1, self.y - 1),
                         (self.x, self.y - 1), (self.x + 1, self.y - 1)):
                if i >= 1 and j >= 1 and i <= 15 and j <= 10:
                    if self.gameboard.occupant(i, j) == 0:
                        potential_squares.append((i, j))
            print potential_squares
            print "Target your Creature in one of the above squares:"
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            if self.holo_choice == "Holo":
                self.gameboard.holo_creature(x, y, self.action_card)
            else:
                if self.rng():
                    self.gameboard.beam_creature(x, y, self.action_card)
                    self.creatures.append(self.action_card)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        # holodetect has global targetting
        elif isinstance(self.action_card, HoloDetect):
            # enemy creatures
            potential_squares = []
            # look at every square on the board
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and not a commander
                        if not isinstance(occ, Commander):
                            # and it's not owned by me
                            if occ.commander != self:
                                # it's targetable
                                potential_squares.append((i + 1, j + 1))
            print potential_squares
            print "Target your HoloDetect at one of the above squares:"
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            # no corpse, just kill the creature
            if self.gameboard.occupant(x, y).holograph == True:
                self.gameboard.kill_creature(x, y)

        # emp has global targetting
        # todo: commander emp
        elif isinstance(self.action_card, EMP):
            # enemy tech creatures + commander
            potential_squares = []
            # all squares
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and a commander or a tech unit
                        if isinstance(occ, Commander) or occ.alignment > 0:
                            # and not owned by me
                            if occ.commander != self:
                                #it's targetable
                                potential_squares.append((i + 1, j + 1))
            print potential_squares
            print "Target your EMP at one of the above squares:"
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            if isinstance(self.gameboard.occupant(x, y), Commander):
                if self.rng():
                    # todo: check commander resistance, potentially kill all tech
                    pass
            else:
                if self.rng():
                    self.gameboard.kill_creature(x, y)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        # virus has global targetting
        # todo: commander virus
        elif isinstance(self.action_card, Virus):
            # enemy life creatures + commander
            potential_squares = []
            # all squares
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and a commander or a life unit
                        if isinstance(occ, Commander) or occ.alignment < 0:
                            # and not owned by me
                            if occ.commander != self:
                                # it's targetable
                                potential_squares.append((i + 1, j + 1))
            print potential_squares
            print "Target your Virus at one of the above squares:"
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            if isinstance(self.gameboard.occupant(x, y), Commander):
                if self.rng():   
                    # todo: check commander resistance, potentially kill all life
                    pass
            else:
                if self.rng():
                    self.gameboard.kill_creature(x, y)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        # fortress is only structure that requires targetting
        elif isinstance(self.action_card, Fortress):
            potential_squares = []
            for i, j in ((self.x - 1, self.y + 1), (self.x, self.y + 1),
                         (self.x + 1, self.y + 1), (self.x - 1, self.y),
                         (self.x + 1, self.y), (self.x - 1, self.y - 1),
                         (self.x, self.y - 1), (self.x + 1, self.y - 1)):
                if i >= 1 and j >= 1 and i <= 15 and i <= 10:
                    if self.gameboard.occupant(i, j) == 0:
                        potential_squares.append((i, j))
            print potential_squares
            print "Target your Fortress in one of the above squares:"
            x = int(raw_input("X: "))
            y = int(raw_input("Y: "))
            if self.rng():
                self.gameboard.occupy(x, y, self.action_card)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        # all other structures require no targetting
        elif isinstance(self.action_card, Structure):

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

            if self.rng():
                if isinstance(self.action_card, ForceField):
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
                        if j >= 1 and i >= 1 and j <= 10 and i <= 15:
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[10 - j]\
                                [i - 1]["alive"] = self.action_card

                elif isinstance(self.action_card, GunTurret):
                    for i, j in ((self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 2), 
                                 (self.x, self.y - 2), (self.x - 2, self.y + 2), 
                                 (self.x + 2, self.y + 2), (self.x - 2, self.y - 2), 
                                 (self.x + 2, self.y - 2)):
                        if j >= 1 and i >= 1 and j <= 10 and i <= 15:
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[10 - j]\
                                [i - 1]["alive"] = GunTurret()

                elif isinstance(self.action_card, SubspaceBeacon):
                    for i, j in ((self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y + 2), 
                                 (self.x, self.y - 2), (self.x - 2, self.y + 2), 
                                 (self.x + 2, self.y + 2), (self.x - 2, self.y - 2), 
                                 (self.x + 2, self.y - 2)):
                        if j >= 1 and i >= 1 and j <= 10 and i <= 15:
                            if self.gameboard.occupant(i, j) == 0:
                                self.gameboard.board[10 - j]\
                                [i - 1]["alive"] = SubspaceBeacon()                

        elif isinstance(self.action_card, Mutate):
            # requires a list of all_creatures
            pass

        elif isinstance(self.action_card, Hypnotize):
            # NEED target x, y
            # self.board[self.height - y][x - 1]["alive"] = \
            # self.board[self.height - y][x - 1]["dead"]
            pass

        elif isinstance(self.action_card, Resurrect):
            # NEED target x, y
            # self.board[self.height - y][x - 1]["alive"] = \
            # self.board[self.height - y][x - 1]["dead"]

            # don't forget to remove the corpse
            # self.board[self.height - y][x - 1]["dead"] = 0
            pass

        elif isinstance(self.action_card, Disrupt):
            # NEED target x, y
            # r = random.randint(5, 13)
            # if (self.occupant(x, y).resist +
            #     self.occupant(x, y).defense) < r:
            #     self.kill_creature(x, y)
            pass

        elif isinstance(self.action_card, Disintegrate):
            # NEED target x, y
            # r = random.randint(7, 17)
            # if (self.occupant(x, y).resist +
            #     self.occupant(x, y).defense) < r:
            #     self.kill_creature(x, y)
            pass

        elif isinstance(self.action_card, Teleport):
            # NEED target x, y
            pass

        elif isinstance(self.action_card, Fire):
            # NEED target x, y
            pass

        elif isinstance(self.action_card, AlienGoo):
            # NEED target x, y
            pass

        # reset for next card choosing
        self.action_card = BlankCard()

    def move(self):
        self.gameboard.print_board()
        pass

# ALL CARDS ARE IN THIS FOLD
class BlankCard(object):
    def __init__(self):
        self.name = ""

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
        self.alignment = 1

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
