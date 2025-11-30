"""
Retro 1970s-style loading screen
"""
import pygame
import config
import time

class LoadingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_time = None
        self.loading_duration = 2.0  # 2 seconds
        self.font_large = None
        self.font_medium = None
        self.animation_frame = 0
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
    
    def start(self):
        """Start the loading screen"""
        self.start_time = time.time()
        self.animation_frame = 0
    
    def is_complete(self):
        """Check if loading is complete"""
        if self.start_time is None:
            return False
        return time.time() - self.start_time >= self.loading_duration
    
    def draw(self):
        """Draw the loading screen with retro animation"""
        if self.font_large is None:
            self.initialize_fonts()
        
        # 1970s retro background
        for y in range(config.SCREEN_HEIGHT):
            ratio = y / config.SCREEN_HEIGHT
            r = int(config.RETRO_BROWN[0] * (1 - ratio) + config.RETRO_BEIGE[0] * ratio)
            g = int(config.RETRO_BROWN[1] * (1 - ratio) + config.RETRO_BEIGE[1] * ratio)
            b = int(config.RETRO_BROWN[2] * (1 - ratio) + config.RETRO_BEIGE[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (config.SCREEN_WIDTH, y))
        
        # Loading text
        loading_text = self.font_large.render("LOADING", True, config.RETRO_ORANGE)
        loading_rect = loading_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(loading_text, loading_rect)
        
        # Animated dots
        self.animation_frame += 1
        dots = "." * ((self.animation_frame // 10) % 4)
        dots_text = self.font_medium.render(dots, True, config.RETRO_YELLOW)
        dots_rect = dots_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(dots_text, dots_rect)
        
        # Progress bar (retro style)
        if self.start_time:
            progress = min((time.time() - self.start_time) / self.loading_duration, 1.0)
            bar_width = 400
            bar_height = 20
            bar_x = (config.SCREEN_WIDTH - bar_width) // 2
            bar_y = config.SCREEN_HEIGHT // 2 + 80
            
            # Draw bar background
            pygame.draw.rect(self.screen, config.BLACK, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, config.RETRO_ORANGE, (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Draw progress
            fill_width = int(bar_width * progress)
            if fill_width > 0:
                pygame.draw.rect(self.screen, config.RETRO_YELLOW, (bar_x + 2, bar_y + 2, fill_width - 4, bar_height - 4))
        
        pygame.display.flip()

