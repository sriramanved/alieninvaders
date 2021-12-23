"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need to be used
in the model, the view, and the controller. As these are spread across multiple modules,
we separate the constants into their own module. This allows all modules to access them.

Dhruv Mittal (dm885) and Ved Sriraman (vs346)
December 8th, 2021
"""
import introcs
import sys

### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
SHIP_WIDTH    = 44
# the height of the paddle
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The image file to use for the ship
SHIP_IMAGE    = 'ship.png'
# The image sprite to use for the ship exploding
SHIP_STRIPE   = 'ship-strip.png'
# The number of lives a ship has
SHIP_LIVES    = 3
# How many seconds a death animation takes
DEATH_SPEED   = 0.3
# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100



### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 16
# the vertical separation between aliens
ALIEN_V_SEP   = 16
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)
ALIEN_IMAGES   = ('alien1.png','alien2.png','alien3.png')
# the number of seconds (float <= 1) between alien steps
ALIEN_SPEED = 1.0


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 16
# the number of pixels to move the bolt per update
BOLT_SPEED  = 10
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5


### GAME CONSTANTS ###

# state before the game has started
STATE_INACTIVE = 0
# state when we are initializing a new wave
STATE_NEWWAVE  = 1
# state when the level is activated and in play
STATE_ACTIVE   = 2
# state when we are are paused between lives
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
#: state when the game is complete (won or lost)
STATE_COMPLETE = 5


### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run python. These arguments are
everything after the word python. So if you start the game typing

    python invaders 3 4 0.5

Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take advantage of
this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW, and ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= 10:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= 15:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed >= 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###

# The alternate images to use in the filmstrip
SHIP_IMAGE    = 'ship-strip.png'

# The alternate images to use in the filmstrip
ALIEN_IMAGES   = ('alien-strip1.png','alien-strip2.png','alien-strip3.png')
# The number of (base) points each alien is worth.  Multiplied by row
ALIEN_POINTS = 10
# The speed up factor for each alien killed.
SPEED_FACTOR = 1.03
# The music volume for each alien step.
STEP_VOLUME = 0.3

# The font choice for labels and messages
ARCADE_FONT = 'Arcade.ttf'
# A large message or label
ARCADE_LARGE  = 60
# A medium message or label
ARCADE_MEDIUM = 48
# A small message or label
ARCADE_SMALL  = 32

# The background color
DARK_GREY = introcs.RGB(32, 32, 32)
# Other useful colors
WHITE_COLOR = introcs.RGB(255, 255, 255)
YELLOW_COLOR = introcs.RGB(255, 255, 0)

# The offset of the top labels from the top of the screen
LABEL_HEIGHT  = 32
# The offset between the score label and the score value
SCORE_OFFSET  = 150
# The position of the lives label
LIVES_MARGIN  = 185
# The offset between the lives label and the lives value
LIVES_OFFSET  = 135

# The width of a message banner
BANNER_WIDTH  = GAME_WIDTH-100
# The height of a message banner
BANNER_HEIGHT = GAME_HEIGHT/4
