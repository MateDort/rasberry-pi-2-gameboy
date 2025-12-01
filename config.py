"""
Configuration constants for the Game Boy Games
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DARK_GREEN = (26, 77, 46)  # #1a4d2e
PURPLE = (139, 0, 255)  # #8b00ff
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RETRO_BROWN = (139, 90, 43)  # #8b5a2b
RETRO_ORANGE = (255, 140, 0)  # #ff8c00
RETRO_YELLOW = (255, 215, 0)  # #ffd700
RETRO_BEIGE = (245, 222, 179)  # #f5deb3

# Flappy Bird Colors
SKY_BLUE = (135, 206, 250)  # Light blue sky
CITY_BLUE = (173, 216, 230)  # Light blue city silhouette
CITY_DARK_BLUE = (135, 206, 250)  # Darker blue for windows
BIRD_YELLOW = (255, 255, 0)  # Yellow bird
BIRD_ORANGE = (255, 165, 0)  # Orange beak
PIPE_GREEN = (34, 139, 34)  # Green pipe
PIPE_DARK_GREEN = (0, 100, 0)  # Darker green outline
PIPE_LIGHT_GREEN = (144, 238, 144)  # Light green highlight
GROUND_BROWN = (222, 184, 135)  # Light brown ground
GROUND_GREEN = (124, 252, 0)  # Green stripe
GROUND_DARK_GREEN = (50, 205, 50)  # Darker green stripe
HORIZON_GREEN = (34, 139, 34)  # Horizon line
PAUSE_RED = (255, 0, 0)  # Red pause button

# Game settings
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # 40 cells wide
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 30 cells tall
SNAKE_SPEED = 10  # Frames per move (lower = faster)
FPS = 60

# Flappy Bird settings
GRAVITY = 0.5  # Gravity strength
BIRD_JUMP_STRENGTH = 8  # Jump velocity
GROUND_HEIGHT = 80  # Height of ground
GROUND_PATTERN_WIDTH = 40  # Width of ground pattern repeat

# Font sizes
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Mario Game Colors
MARIO_RED = (220, 0, 0)  # Mario's red
MARIO_BLUE = (0, 100, 200)  # Mario's blue
MARIO_BROWN = (139, 90, 43)  # Brown for blocks/enemies
MARIO_YELLOW = (255, 215, 0)  # Yellow for question blocks
MARIO_GREEN = (34, 139, 34)  # Green for pipes
MARIO_ORANGE = (255, 140, 0)  # Orange for fireballs
MARIO_SKY = (135, 206, 250)  # Sky blue background
MARIO_GROUND = (139, 90, 43)  # Ground brown
GOOMBA_BROWN = (101, 67, 33)  # Goomba color
KOOPA_GREEN = (0, 150, 0)  # Koopa shell color
MUSHROOM_RED = (255, 0, 0)  # Mushroom red
MUSHROOM_WHITE = (255, 255, 255)  # Mushroom white
COIN_YELLOW = (255, 215, 0)  # Coin color

# Mario Physics
MARIO_JUMP_STRENGTH = 12  # Jump velocity
MARIO_RUN_SPEED = 4  # Horizontal movement speed
MARIO_GRAVITY = 0.6  # Gravity strength
MARIO_MAX_FALL_SPEED = 10  # Maximum falling speed

# Mario Sizes
MARIO_SMALL_WIDTH = 24
MARIO_SMALL_HEIGHT = 32
MARIO_LARGE_WIDTH = 24
MARIO_LARGE_HEIGHT = 48

# Enemy Settings
GOOMBA_SPEED = 1.5
KOOPA_SPEED = 1.5
KOOPA_SHELL_SPEED = 5  # Speed when shell is kicked

# Block/Coin Sizes
BLOCK_SIZE = 32  # Size of blocks (32x32)
COIN_SIZE = 16  # Size of coins (16x16)

# Power-up Settings
FIREBALL_SPEED = 6  # Fireball horizontal speed
INVINCIBILITY_TIME = 120  # Frames of invincibility after hit (2 seconds at 60fps)

# Mario Game Settings
MARIO_START_LIVES = 3  # Starting number of lives
COINS_PER_LIFE = 100  # Coins needed for extra life

