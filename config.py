"""
Configuration constants for the Game Boy Snake Game
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

# Game settings
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # 40 cells wide
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 30 cells tall
SNAKE_SPEED = 10  # Frames per move (lower = faster)
FPS = 60

# Font sizes
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

