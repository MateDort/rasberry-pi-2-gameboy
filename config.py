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

