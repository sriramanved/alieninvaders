"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Dhruv Mittal (dm885) and Ved Sriraman (vs346)
December 8th, 2021
"""
from game2d import *
from consts import *
from models import *
import random
import math

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _direction: checks which direction the aliens are moving
    # Invariant: _direction is a boolean
    #
    # Attribute _randomnum: stores a random number between 1 and BOLT_RATE
    # Invariant: _randomnum is an int between 1 and BOLT_RATE
    #
    # Attribute _xp: the amount of rows in the stripe image
    # Invariant: _xp is an int > 0
    #
    # Attribute _yp: the amount of columns in the stripe image
    # Invariant: _yp is an int > 0
    #
    # Attribute _animator: the animation coroutine
    # Invariant: _animator is either none or a coroutine
    #
    # Attribute _shipdead: determines whether or not the ship is None (just killed)
    # Invariant: _shipdead is a boolean value (True if dead)
    #
    # Attribute _xc: the initial x position of the ship when a new ship is created
    # Invariant: _xc is an int or a float >= 0
    #
    # Attribute _yc: the initial y position of the ship when a new ship is created
    # Invariant: _yc is an int or a float >= 0
    #
    # Attribute _win: used to determine whether or not the player has won the game
    # Invariant: _win is a boolean value

    # Attribute _loss: used to determine whether or not the player has won the game
    # Invariant: _loss is a boolean value

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getlives(self):
        """
        Returns the attribute _lives for the Wave object
        """
        return self._lives

    def setlives(self, x):
        """
        Modifies the attribute _lives for the Wave object

        Parameter x: Used to set the attribute _lives.
        Precondition: x is an int >= 0
        """
        self._lives = x

    def getshipdead(self):
        """
        Returns the attribute _shipdead for the Wave object
        """
        return self._shipdead

    def setshipdead(self, x):
        """
        Modifies the attribute _shipdead for the Wave object

        Parameter x: Used to set the attribute _shipdead.
        Precondition: x is a boolean value
        """
        self._shipdead = x

    def getwin(self):
        """
        Returns the attribute _dead for the Wave object
        """
        return self._win

    def getloss(self):
        """
        Returns the attribute _loss for the Wave object
        """
        return self._loss

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes all attributes used in the class Wave.
        """
        self._aliens = self._alienswave()
        self._ship = Ship(inputx = GAME_WIDTH/2, inputy = SHIP_HEIGHT + SHIP_HEIGHT/2,
        inputwidth = SHIP_WIDTH, inputheight = SHIP_HEIGHT, inputsource = \
        SHIP_IMAGE, xp = 2, yp = 4)

        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], \
        linewidth = 2, linecolor = [0,0,0,1])
        self._bolts = []

        self._time = 0
        self._direction = False
        self._lives = SHIP_LIVES -1

        self._randomnum = random.randrange(1, BOLT_RATE + 1)

        self._xp = 2
        self._yp = 4

        self._animator = None

        self._shipdead = False

        self._xc = 0
        self._yc = 0

        self._win = False
        self._loss = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates the ship, aliens, and laser bolts.

        Uses helper methods to detect ship and alien collisions, start and move
        ship, bolts and aliens. Also checks whether a win or loss has occurred.
        Contain the driver for the coroutine.

        Parameter input: the id folder of the interaction
        Precondition: input is a instance of GInput

        Parameter dt: The time in seconds since update in the class Invaders
        last updated
        Precondition: dt is a number (int or float)
        """
        if self._animator is None:
            self._moveship(input, dt)
            self._existsPlayerBolt()
            self._boltstart(input)  #Creates bolts
            self._boltmove()  #Moves bolts
            self._boltdelete()  #Deletes bolts off screen
            self._movealien(dt)
            self._alienshoot(dt)
            self._shipcollision()
            self._aliencollision()
            self._checkalienline()
        else:
            # self._animator = self.animate(dt)
            self._runAnimator(dt)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, alien, and bolt objects in view. Called by the draw
        method in app.py.
        """

        for a in range(len(self._aliens)):
            for b in range(len(self._aliens[a])):
                if self._aliens[a][b] != None:
                    self._aliens[a][b].draw(view)

        if not (self._ship is None):
            self._ship.draw(view)

        self._dline.draw(view)

        for a in range(len(self._bolts)):
            self._bolts[a].draw(view)

 ##### Hidden HELPER METHODS BELOW #####
    def _alienswave(self):
        """
        This method helps the initializer by creating a table of aliens
        according to the specifications of assignment7. The rows of aliens
        are created from the bottom up.
        """

        img = ['alien1.png', 'alien1.png', 'alien2.png', 'alien2.png', \
        'alien3.png', 'alien3.png']
        pic = 0
        b = GAME_HEIGHT - (ALIEN_CEILING + ALIEN_HEIGHT/2) - ((ALIEN_ROWS - 1) \
         * (ALIEN_HEIGHT + ALIEN_V_SEP))
        rows = []
        for y in range(ALIEN_ROWS):
            row = []
            a = ALIEN_H_SEP + ALIEN_WIDTH/2
            for x in range(ALIENS_IN_ROW):
                alien = Alien(inputx = a, inputy = b, inputwidth = ALIEN_WIDTH,
                inputheight = ALIEN_HEIGHT, inputsource = img[pic])
                row.append(alien)
                a = a + ALIEN_WIDTH + ALIEN_H_SEP
            rows.append(row)
            b = b + (ALIEN_HEIGHT + ALIEN_V_SEP)
            pic = pic + 1
            if pic > 5:
                pic = 0
        return rows

    def _movealien(self, dt):
        """
        This method moves the Aliens back and forth across the game window
        according to the specificaions of assignment7.

        Parameter dt: The time in seconds since update in the class Invaders
        last updated
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        if (self._time >= ALIEN_SPEED): # condition to move is True
            if not self._direction:
                if GAME_WIDTH - (self._mostrightalien() + ALIEN_WIDTH/2 + ALIEN_H_WALK) < ALIEN_H_SEP:
                    self._movedownthenleft()
                else:
                    for row in range(len(self._aliens)):
                        for col in range(len(self._aliens[row])):
                            if self._aliens[row][col] != None:
                                self._aliens[row][col].right += ALIEN_H_WALK
            elif self._direction:
                if self._mostleftalien() - ALIEN_WIDTH/2 - ALIEN_H_WALK < ALIEN_H_SEP:
                    self._movedownthenright()
                else:
                    for row in range(len(self._aliens)):
                        for col in range(len(self._aliens[row])):
                            if self._aliens[row][col] != None:
                                self._aliens[row][col].left -= ALIEN_H_WALK

    def _movedownthenleft(self):
        """
        Moves the aliens down once it has been determined that there is no space
        to move to the right anymore.
        """
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if self._aliens[row][col] != None:
                    self._aliens[row][col].bottom -= ALIEN_V_WALK
        self._direction = not self._direction

    def _movedownthenright(self):
        """
        Moves the aliens down once it has been determined that there is no space
        to move to the left anymore.
        """
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if self._aliens[row][col] != None:
                    self._aliens[row][col].bottom -= ALIEN_V_WALK
            # alien.left += ALIEN_H_SEP
            # self._aliens[row][col].x += ALIEN_H_SEP
        self._direction = not self._direction

    def _mostleftalien(self):
        """
        Returns left most alien's x position.
        """
        min = GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if alien.getalienx() < min:
                        min = alien.getalienx()
        return min

    def _mostrightalien(self):
        """
        Returns right most alien's x position.
        """
        max = 0
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if alien.getalienx() > max:
                        max = alien.getalienx()
        return max

    def _moveship(self, input, dt):
        """
        Moves the player ship to the left and right in accordance to the player
        pressing the "left" and "right" arrow keys.

        Parameter input: the id folder of the interaction
        Precondition: input is a instance of GInput
        """
        if self._ship != None:
            if min(self._ship.x - self._ship.width, 0) == 0 and \
            max(self._ship.x + self._ship.width, GAME_WIDTH) == GAME_WIDTH:
                if input.is_key_down('right'):
                    self._ship.x += SHIP_MOVEMENT
                if input.is_key_down('left'):
                    self._ship.x -= SHIP_MOVEMENT

            if min(self._ship.x - self._ship.width, 0) \
            == self._ship.x - self._ship.width:
                if input.is_key_down('right'):
                    self._ship.x += SHIP_MOVEMENT

            if max(self._ship.x + self._ship.width, GAME_WIDTH) \
            == self._ship.x + self._ship.width:
                if input.is_key_down('left'):
                    self._ship.x -= SHIP_MOVEMENT
        else:
            self._ship = Ship(inputx = self._xc, inputy = self._yc,
            inputwidth = SHIP_WIDTH, inputheight = SHIP_HEIGHT, \
            inputsource = SHIP_STRIPE, xp = 2, yp = 4)
            self._animator = self._animate()
            next(self._animator)

    def _boltstart(self, input):
        """
        Creates a Bolt object infront of the player ship when the player presses
        the "up" arrow key and there are no other player bolts on the game window.

        Parameter input: the id folder of the interaction
        Precondition: input is a instance of GInput
        """

        if input.is_key_down('up') and self._existsPlayerBolt() == False:
            self._bolts.append(Bolt(inputx = self._ship.x, \
            inputy = SHIP_HEIGHT + SHIP_HEIGHT + BOLT_HEIGHT/2, inputwidth = \
            BOLT_WIDTH, inputheight = BOLT_HEIGHT, inputfillcolor = 'red', \
            velocity = BOLT_SPEED))

    def _boltmove(self):
        """
        Moves both the player bolts up and alien bolts down at the speed
        BOLT_SPEED and -BOLT_SPEED respectively
        """

        for bolt in range(len(self._bolts)):
            if self._bolts[bolt]._velocity == BOLT_SPEED:
                self._bolts[bolt].y += BOLT_SPEED
            if self._bolts[bolt]._velocity == -BOLT_SPEED:
                self._bolts[bolt].y += -BOLT_SPEED

    def _boltdelete(self):
        """
        Deletes any player or alien bolts once they are no longer within
        the bounds of the game window.
        """
        b = []
        for bolt in range(len(self._bolts)):
            if self._bolts[bolt].y < GAME_HEIGHT and \
            self._bolts[bolt]._velocity == BOLT_SPEED:
                b.append(self._bolts[bolt])
            if self._bolts[bolt].y > 0 and \
            self._bolts[bolt]._velocity == -BOLT_SPEED:
                b.append(self._bolts[bolt])
        self._bolts = b

    def _existsPlayerBolt(self):
        """
        Returns True if there is a player bolt already within the bounds of the
        game window. False otherwise.
        """

        result = False
        for bolt in range(len(self._bolts)):
            if self._bolts[bolt]._velocity == BOLT_SPEED:
                result = True
            else:
                result = False
        return result

    def _alienshoot(self, dt):
        """
        This method is responsible for randomly deciding when bolts will be shot
        by the aliens and then creating the bolt shot by the given randomly
        chosen alien.

        Parameter dt: The time in seconds since update in the class Invaders
        last updated
        Precondition: dt is a number (int or float)
        """
        if self._time >= ALIEN_SPEED and self._randomnum == 0:
            chosenalien = self._randomalien()

            if type(chosenalien) == int:
                pass

            else:
                self._bolts.append(Bolt(inputx = chosenalien.x, \
                inputy = chosenalien.y - ALIEN_WIDTH/2, \
                inputwidth = BOLT_WIDTH, inputheight = BOLT_HEIGHT, \
                inputfillcolor = 'red', velocity = -BOLT_SPEED))
                self._time = 0
                self._randomnum = random.randrange(1, BOLT_RATE + 1)

        if self._time >= ALIEN_SPEED and self._randomnum != 0:
            self._randomnum = self._randomnum - 1
            self._time = 0

    def _randomalien(self):
        """
        This is a helper method for _alienshoot. This function chooses the
        frontmost alien on a random column to shoot. If there are no Aliens left,
        this function triggers the end game state.
        """
        a = 0
        b = random.randrange(0,ALIENS_IN_ROW)
        c = 0

        while a < ALIEN_ROWS  and c == 0:
            if self._aliens[a][b] != None:
                return self._aliens[a][b]

            elif a == ALIEN_ROWS - 1 and self._aliens[a][b] == None:
                a = 0
                b = random.randrange(0,ALIENS_IN_ROW)

            if self._checkaliensthere():
                self._win = True
                c = 1
                return 5

            a = a + 1

    def _checkaliensthere(self):
        """
        This is a helper method for _randomalien. This function repeatedly
        checks all the aliens to ensure they are still there. When all aliens are
        dead this function returns True, False otherwise.
        """
        res = True
        for a in range(len(self._aliens)):
            for b in range(len(self._aliens[a])):
                if self._aliens[a][b] != None:
                    res = False
        return res

    def _shipcollision(self):
        """
        This function detects if the ship has been hit by an alien bullet, and
        then sets the ship to None and deletes the alien bullet.
        """
        for bolt in range(len(self._bolts)):
            if self._ship != None:
                if self._ship.collides(self._bolts[bolt]):
                    self._xc = self._ship.x
                    self._yc = self._ship.y
                    self._ship = None
                    del(self._bolts[bolt])

    def _aliencollision(self):
        """
        This function detects if any alien has been hit by an ship bullet, and
        then sets that alien to None and deletes the ship bullet.
        """
        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                    for bolt in range(len(self._bolts)):
                        if self._aliens[row][alien] != None:
                            if self._aliens[row][alien].collides\
                            (self._bolts[bolt]):
                                self._aliens[row][alien] = None
                                del(self._bolts[bolt])

    def _runAnimator(self, dt):
        """
        The driver for the animation coroutine

        Parameter dt: The number of seconds since the last animation frame
        Precondition: dt is an float >= 0
        """
        try:
            self._animator.send(dt)
        except (RuntimeError, StopIteration):
            self._ship.frame = 0
            self._animator = None
            self._bolts.clear()

    def _animate(self):
        """
        The animation coroutine.
        This has a yield expression that receives the dt
        (and does NOT yield anything back the parent).
        """
        time = 0
        animating = True
        while animating:
            # Get the current time
            dt = (yield)
            time += dt
            x = time/DEATH_SPEED
            amount = x*self._xp*self._yp

            if time > DEATH_SPEED:
                animating = False
                self._shipdead = True

                raise StopIteration
            else:
                self._ship.frame = math.ceil(amount) - 1

    def _checkalienline(self):
        """
        Determines whether or not any of the aliens have crossed the barrier
        line. This should set the loss attribute to true to indicate that the player
        has lost the game.
        """
        r = False
        for a in range(len(self._aliens)):
            for b in range(len(self._aliens[a])):
                if self._aliens[a][b] != None:
                    if self._aliens[a][b].y - ALIEN_HEIGHT/2 < DEFENSE_LINE:
                        r = True
        if r == True:
            self._loss = True
