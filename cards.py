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
        self.hologram = False
        self.gameboard = 0
        self.x = 0
        self.y = 0
        self.commander = 0
        self.moved = False

    def squares_in_range(self, r):
        """
        This function creates an array that displays the minimum number of
        movements it would take to move to that targetted square if lateral
        movements take 1 unit and diagonal movements take 1.5 units. It then
        checks all the squares in the array against the desired reach and 
        returns a list of the squares which could be reached.
        """
        # only create a square for as far as we need to
        dimension = r + 1

        # create the square
        moves = [[0.0 for j in range(dimension)] for i in range(dimension)]

        # fill the square with the correct values
        for i in range(dimension):
            for j in range(dimension):
                if j == 0 or i == 0:
                    moves[i][j] = float(i + j)
                elif j <= i:
                    moves[i][j] = moves[i][j - 1] + 0.5
                else:
                    moves[i][j] = moves[i][j - 1] + 1

        # make sure they're rounded down to integer after generation
        for i in range(dimension):
            for j in range(dimension):
                moves[i][j] = int(moves[i][j])

        # create the list of squares in range
        in_range = []
        for i in range(dimension):
            for j in range(dimension):
                if moves[i][j] <= r:
                    if (self.x + j <= 15 and self.x + j >= 1 and 
                        self.y + i <= 10 and self.y + i >= 1):
                        in_range.append((self.x + j, self.y + i))

                    if (self.x - j <= 15 and self.x - j >= 1 and 
                        self.y - i <= 10 and self.y - i >= 1):
                        in_range.append((self.x - j, self.y - i))

                    if (self.x + j <= 15 and self.x + j >= 1 and 
                        self.y - i <= 10 and self.y - i >= 1):
                        in_range.append((self.x + j, self.y - i))

                    if (self.x - j <= 15 and self.x - j >= 1 and 
                        self.y + i <= 10 and self.y + i >= 1):
                        in_range.append((self.x - j, self.y + i))
                        
        in_range = list(set(in_range))
        in_range.remove((self.x, self.y))

        return in_range
        
    def squares_seen(self):
        """
        This function is Bresenham's line creation algorithm. It takes two
        end-points of a line on a grid and determines which points to fill in
        between the endpoints to make the best-fitting line. The points returned
        can be checked for occupants to determine sight.
        """

        seen = []

        for i in range(10):
            for j in range(15):
                x1, y1 = (j + 1, 10 - i)
                xorig, yorig = x1, y1
                x0, y0 = (self.x, self.y)

                if x0 == x1 and y0 == y1:
                    continue
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
                for x in range(x0, x1 + 1):
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
                    if error > 0.5:
                        y += ystep
                        error -= 1
                # our range didn't include the last point, and this pop will also
                # remove the first point. this will result in only evaluating the
                # squares between the creature and the point for obstructions
                line.pop(0)
                line.pop()
                # let's assume at first that our source can see the destination
                square_seen = True
                # now check every point in the line for obstructions, and if there are
                # any, flag seen as false because our source can't see the destination
                for point in line:
                    if self.gameboard.occupant(point[0], point[1]) != 0:
                        square_seen = False

                if square_seen == True:
                    seen.append((xorig, yorig))
        return seen

    def move(self):
        if self.flight == False:
            movement = float(self.speed)
            self.moved = True
            lateral_squares = []
            diagonal_squares = []
            attackable_squares = []
            # check the 8 surrounding squares for vacancies or enemies to attack
            for square in self.squares_in_range(1):
                occ = self.gameboard.occupant(square[0], square[1])
                if (isinstance(occ, Creature) and 
                    occ.commander != self.commander):
                    attackable_squares.append((square[0], square[1]))
                elif occ == 0:
                    if square[0] == self.x or square[1] == self.y:
                        lateral_squares.append((square[0], square[1]))
                    else:
                        diagonal_squares.append((square[0], square[1]))
            movable_squares = lateral_squares + diagonal_squares
            print movable_squares + attackable_squares
            print "Where would you like to move/attack?"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            # we're attacking an enemy square
            if (x, y) in attackable_squares:
                self.attack(x, y)
                return

            if (x, y) in movable_squares:
                self.gameboard.occupy(self.x, self.y, 0)
                self.gameboard.occupy(x, y, self)
                if self.x == x or self.y == y:
                    movement -= 1
                else:
                    movement -= 1.5
                self.x, self.y = x, y
                # check our landing point for engagements
                engaged = False
                for square in self.squares_in_range(1):
                    occ = self.gameboard.occupant(square[0], square[1])
                    if (isinstance(occ, Creature) and 
                        occ.commander != self.commander):
                        engaged = True
                if engaged == True:
                    self.gameboard.message = "YOU ARE ENGAGED TO AN ENEMY"
                    self.gameboard.print_board()
                    # check the 8 surrounding squares for vacancies or enemies to attack
                    attackable_squares = []
                    for square in self.squares_in_range(1):
                        occ = self.gameboard.occupant(square[0], square[1])
                        if (isinstance(occ, Creature) and 
                            occ.commander != self.commander):
                            attackable_squares.append((square[0], square[1]))
                    print attackable_squares
                    print "Which square would you like to attack?"
                    x = raw_input("X: ")
                    if x == "q" or x == "":
                        return
                    x = int(x)
                    y = raw_input("Y: ")
                    if y == "q" or y == "":
                        return
                    y = int(y)
                    # we're attacking an enemy square
                    if (x, y) in attackable_squares:
                        self.attack(x, y)
                        return

            while movement >= 1:
                lateral_squares = []
                diagonal_squares = []
                movable_squares = []
                 # check the 8 surrounding squares for vacancies
                for square in self.squares_in_range(1):
                    occ = self.gameboard.occupant(square[0], square[1])
                    if occ == 0:
                        if square[0] == self.x or square[1] == self.y:
                            lateral_squares.append((square[0], square[1]))
                        else:
                            diagonal_squares.append((square[0], square[1]))
                movable_squares = lateral_squares + diagonal_squares
                if movement % 1 == 0:
                    self.gameboard.message = "%i MOVEMENT LEFT" % movement
                else:
                    self.gameboard.message = "%.1f MOVEMENT LEFT" % movement
                self.gameboard.print_board()
                
                print movable_squares
                print "Where would you like to move?"
                x = raw_input("X: ")
                if x == "q" or x == "":
                    return
                x = int(x)
                y = raw_input("Y: ")
                if y == "q" or y == "":
                    return
                y = int(y)
                if (x, y) in movable_squares:
                    self.gameboard.occupy(self.x, self.y, 0)
                    self.gameboard.occupy(x, y, self)
                    if self.x == x or self.y == y:
                        movement -= 1
                    else:
                        movement -= 1.5
                    self.x, self.y = x, y
                    # check our landing point for engagements
                    engaged = False
                    for square in self.squares_in_range(1):
                        occ = self.gameboard.occupant(square[0], square[1])
                        if (isinstance(occ, Creature) and 
                            occ.commander != self.commander):
                            engaged = True
                    if engaged == True:
                        self.gameboard.message = "YOU ARE ENGAGED TO AN ENEMY"
                        self.gameboard.print_board()
                        # check the 8 surrounding squares for vacancies or enemies to attack
                        attackable_squares = []
                        for square in self.squares_in_range(1):
                            occ = self.gameboard.occupant(square[0], square[1])
                            if (isinstance(occ, Creature) and 
                                occ.commander != self.commander):
                                attackable_squares.append((square[0], square[1]))
                        print attackable_squares
                        print "Which square would you like to attack?"
                        x = raw_input("X: ")
                        if x == "q" or x == "":
                            return
                        x = int(x)
                        y = raw_input("Y: ")
                        if y == "q" or y == "":
                            return
                        y = int(y)
                        # we're attacking an enemy square
                        if (x, y) in attackable_squares:
                            self.attack(x, y)
                            return

        else:
            self.moved = True
            attackable_squares = []
            movable_squares = []
            # check all surrounding squares for vacancies or enemies to attack
            for square in self.squares_in_range(self.speed):
                occ = self.gameboard.occupant(square[0], square[1])
                if isinstance(occ, Creature) and occ.commander != self:
                    attackable_squares.append((square[0], square[1]))
                elif occ == 0:
                    movable_squares.append((square[0], square[1]))
            print movable_squares + attackable_squares
            print "Where would you like to move/attack?"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            # we're attacking an enemy square
            if (x, y) in attackable_squares:
                self.attack(x, y)
                return

            if (x, y) in movable_squares:
                self.gameboard.occupy(self.x, self.y, 0)
                self.gameboard.occupy(x, y, self)
                self.x, self.y = x, y
                # check our landing point for engagements
                engaged = False
                for square in self.squares_in_range(1):
                    occ = self.gameboard.occupant(square[0], square[1])
                    if (isinstance(occ, Creature) and 
                        occ.commander != self.commander):
                        engaged = True
                if engaged == True:
                    self.gameboard.message = "YOU ARE ENGAGED TO AN ENEMY"
                    self.gameboard.print_board()
                    # check the 8 surrounding squares for vacancies or enemies to attack
                    attackable_squares = []
                    for square in self.squares_in_range(1):
                        occ = self.gameboard.occupant(square[0], square[1])
                        if (isinstance(occ, Creature) and 
                            occ.commander != self.commander):
                            attackable_squares.append((square[0], square[1]))
                    print attackable_squares
                    print "Which square would you like to attack?"
                    x = raw_input("X: ")
                    if x == "q" or x == "":
                        return
                    x = int(x)
                    y = raw_input("Y: ")
                    if y == "q" or y == "":
                        return
                    y = int(y)
                    y = int(y)
                    # we're attacking an enemy square
                    if (x, y) in attackable_squares:
                        self.attack(x, y)
                        return

        if self.range > 1:
            self.gameboard.print_board()
            in_range = self.squares_in_range(self.range)
            seen = self.squares_seen()
            a = list(set(in_range) & set(seen))
            attackable_squares = a[:]
            for square in a:
                occ = self.gameboard.occupant(square[0], square[1])
                # TODO - FIX FOR SUBSPACE/TURRET
                if not isinstance(occ, Creature):
                    attackable_squares.remove((square[0], square[1]))
                    print "rm %i, %i. not creature" % (square[0], square[1])
                if occ != 0:
                    if occ.commander == self.commander:
                        attackable_squares.remove((square[0], square[1]))
                        print "rm %i, %i. not mine" % (square[0], square[1])
            print attackable_squares
            print "Where would you like to send your ranged attack?"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if (x, y) in attackable_squares:
                self.range_attack(x, y)
                return

    def attack(self, x, y):
        strength = self.strength
        defense = self.gameboard.occupant(x, y).defense
        added_chance = (strength - defense)
        r = random.randint(1, 10)
        if 0.5 + added_chance >= r:
            self.gameboard.kill_creature(x, y)
            self.gameboard.occupy(self.x, self.y, 0)
            self.gameboard.occupy(x, y, self)
            self.x = x
            self.y = y

    def range_attack(self, x, y):
        strength = self.rstr
        defense = self.gameboard.occupant(x, y).defense
        added_chance = (strength - defense)
        r = random.randint(1, 10)
        if 0.5 + added_chance >= r:
            self.gameboard.kill_creature(self.gameboard.occupant(x, y))
            self.gameboard.occupy(self.x, self.y, 0)
            self.gameboard.occupy(x, y, self)
            self.x = x
            self.y = y


class Commander(Creature):
    """This creature is a commander."""
    def __init__(self):
        self.name = "Commander"
        self.strength = 5
        self.defense = 5
        self.speed = 1
        self.resist = 7
        self.range = 0
        self.flight = False
        self.on_mount = False
        self.x = 0
        self.y = 0
        self.hand = self.create_hand()
        self.creatures = [self]
        self.dead_creatures = []
        self.commander = self
        self.hologram = False
        self.moved = False
        self.action_card = BlankCard()
        self.holo_choice = "q"
        self.alignment = 0

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
        while (isinstance(self.action_card, BlankCard)):
            self.gameboard.message = "%s's TURN" % self.name
            self.gameboard.print_board()
            self.print_hand()
            i = raw_input("Which number card would you like to play? ")
            if i == "q" or i == "":
                return
            i = int(i) - 1
            self.action_card = self.hand[i]
            if isinstance(self.action_card, Creature):
                self.holo_choice = raw_input('Do you want to' \
                                             ' "Beam" or "Holo"? ')
                if self.holo_choice == "q" or self.holo_choice == "":
                    self.action_card = BlankCard()
                    self.choose_card()
                    return


    def target_card(self):
        self.gameboard.message = "%s's TURN" % self.name
        self.gameboard.print_board()

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
                    self.rstr = self.strength

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
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if self.holo_choice == "Holo":
                self.gameboard.holo_creature(x, y, self.action_card)
                self.creatures.append(self.action_card)
            else:
                if self.rng():
                    self.gameboard.beam_creature(x, y, self.action_card)
                    self.creatures.append(self.action_card)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

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
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            # no corpse, just kill the creature
            if self.gameboard.occupant(x, y).hologram == True:
                self.gameboard.kill_creature(x, y)

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
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if isinstance(self.gameboard.occupant(x, y), Commander):
                if self.rng():
                    # 20% chance, 10% chance with symbiont
                    r = random.randint(4, 8)
                    if self.gameboard.occupant(x, y).resist <= r:
                        # get the commanders creatures
                        c_list = self.gameboard.occupant(x, y).creatures
                        for c in c_list:
                            # if they're tech
                            if c.alignment > 0:
                                # kill them
                                self.gameboard.kill_creature(c.x, c.y)

            else:
                if self.rng():
                    self.gameboard.kill_creature(x, y)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

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
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if isinstance(self.gameboard.occupant(x, y), Commander):
                if self.rng():
                    # 20% chance, 10% chance with symbiont
                    r = random.randint(4, 8)
                    if self.gameboard.occupant(x, y).resist <= r:
                        # get the commanders creatures
                        c_list = self.gameboard.occupant(x, y).creatures
                        for c in c_list:
                            # if they're lifeforce
                            if c.alignment < 0:
                                # kill them
                                self.gameboard.kill_creature(c.x, c.y)
            else:
                if self.rng():
                    self.gameboard.kill_creature(x, y)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Fortress):
            potential_squares = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (self.y + i >= 1 and self.x + j >= 1 and 
                        self.y + i <= 10 and self.x + j <= 15):
                        if self.gameboard.occupant(self.x + j, self.y + i) == 0:
                            potential_squares.append((self.x + j, self.y + i))
            print potential_squares
            print "Target your Fortress in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if self.rng():
                self.gameboard.occupy(x, y, self.action_card)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        # todo: figure out how to make gun turrets work
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

        # todo: big picture: make sure status messages work
        elif isinstance(self.action_card, Mutate):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and not a commander
                        if not isinstance(occ, Commander):
                            # it's targetable
                            potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Mutate in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if self.rng():
                all_creatures = [AlienHatchling(), Probe(), Droid(), 
                                 SlimeBlob(), LaserRobot(), FloatingEye(), 
                                 FaceGrabber(), Jeep(), SlimeWarrior(), Drone(), 
                                 SentryRobot(), Alien(), FireFox(), 
                                 SlimeBeast(), Hovership(), MutantMount(), 
                                 Cyborg(), HoverTank(), MiningDroid(), Tank(), 
                                 FlyingSlime(), PsiLord(), PsiWarrior(), 
                                 AcidSpitter(), Mutant(), AlienQueen(), 
                                 MechWarrior(), Tentacle(), Predator(),
                                 Spideroid()]
                replacement = random.choice(all_creatures)
                copy = self.gameboard.occupant(x, y)
                self.gameboard.occupy(x, y, replacement)
                replacement.hologram = copy.hologram
                replacement.gameboard = copy.gameboard
                replacement.x = copy.x
                replacement.y = copy.y
                replacement.commander = copy.commander
                copy.commander.creatures.append(replacement)
                copy.commander.creatures.remove(copy)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Hypnotize):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and not a commander
                        if not isinstance(occ, Commander):
                            # and not owned by me
                            if occ.commander != self:
                                # it's targetable
                                potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Hypnotize in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            # always hypnotize probes, 1/7 chance to get pred/spider
            occ = self.gameboard.occupant(x, y)
            r = random.randint(2, 8)
            if occ.resist <= r:
                occ.commander.creatures.remove(occ)
                self.creatures.append(occ)
                occ.commander = self

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Resurrect):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    dead_occ = self.gameboard.dead_occupant(i + 1, j + 1)
                    # if nothing is alive
                    if occ == 0:
                        # and something is dead
                        if isinstance(dead_occ, Creature):
                            # it's targetable
                            potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Resurrect in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if self.rng():
                dead_occ = self.gameboard.dead_occupant(x, y)
                dead_occ.commander.dead_creatures.remove(dead_occ)
                dead_occ.commander = self
                dead_occ.commander.creatures.append(dead_occ)
                self.gameboard.occupy(x, y, dead_occ)
                #  don't forget to remove the corpse
                self.gameboard.dead_occupy(x, y, 0)

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Disrupt):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and not owned by me
                        if occ.commander != self:
                            # it's targetable
                            potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Disrupt in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            occ = self.gameboard.occupant(x, y)
            r = random.randint(5, 13)
            if (occ.resist + occ.defense) < r:
                self.gameboard.kill_creature(x, y)
            
            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Disintegrate):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if it's a creature
                    if isinstance(occ, Creature):
                        # and not owned by me
                        if occ.commander != self:
                            # it's targetable
                            potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Disintegrate in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            occ = self.gameboard.occupant(x, y)
            r = random.randint(7, 17)
            if (occ.resist + occ.defense) < r:
                self.gameboard.kill_creature(x, y)
            
            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Teleport):
            targetable_squares = []
            rangelist = self.squares_in_range(self.action_card.cast_range)
            sightlist = self.squares_seen()
            targetable_squares = list(set(rangelist) & set(sightlist))
            potential_squares = []
            for j in range(10):
                for i in range(15):
                    # shorten down the code
                    occ = self.gameboard.occupant(i + 1, j + 1)
                    # if the square is empty
                    if occ == 0:
                        # it's a valid target
                        potential_squares.append((i + 1, j + 1))
            print list(set(potential_squares) & set(targetable_squares))
            print "Target Teleport in one of the above squares:"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            if self.rng():
                self.gameboard.occupy(x, y, self)
                self.gameboard.occupy(self.x, self.y, 0)
                self.x = x
                self.y = y

            # remove played card from hand
            self.hand[self.hand.index(self.action_card)] = BlankCard()

        elif isinstance(self.action_card, Fire):
            # NEED target x, y
            pass

        elif isinstance(self.action_card, AlienGoo):
            # NEED target x, y
            pass

        # reset for next card choosing
        self.action_card = BlankCard()

    def move_phase(self):
        # number of creatures to move
        for _ in range(len(self.creatures)):
            self.gameboard.message = "%s's TURN" % self.name
            self.gameboard.print_board()
            # print each creature's coordinates
            for creature in self.creatures:
                if not creature.moved:
                    print str((creature.x, creature.y)) ,
            print
            print "Which creature would you like to move"
            x = raw_input("X: ")
            if x == "q" or x == "":
                return
            x = int(x)
            y = raw_input("Y: ")
            if y == "q" or y == "":
                return
            y = int(y)
            movable_squares = []
            attackable_squares = []
            moving_creature = self.gameboard.occupant(x, y)
            moving_creature.move()
            


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
        super(Alien, self).__init__("Alien", 0.7, 3, 3, 2, 5, -2)

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
