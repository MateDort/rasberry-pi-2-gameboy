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
        
        # 1970s style background - dark green with pattern
        self.screen.fill(config.DARK_GREEN)
        
        # Add some 1970s style pattern elements
        # Draw diagonal lines for retro effect
        for i in range(0, config.SCREEN_WIDTH + config.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 60, 35), 
                           (i, 0), (i - config.SCREEN_HEIGHT, config.SCREEN_HEIGHT), 1)
        
        # Draw decorative borders
        pygame.draw.rect(self.screen, config.BLACK, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 8)
        pygame.draw.rect(self.screen, config.PURPLE, (10, 10, config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 20), 3)
        
        # Loading text with 1970s style - outlined
        loading_text = self.font_large.render("LOADING", True, config.PURPLE)
        loading_rect = loading_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
        # Draw black outline
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    outline_rect = loading_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_text = self.font_large.render("LOADING", True, config.BLACK)
                    self.screen.blit(outline_text, outline_rect)
        self.screen.blit(loading_text, loading_rect)
        
        # Animated dots
        self.animation_frame += 1
        dots = "." * ((self.animation_frame // 10) % 4)
        dots_text = self.font_medium.render(dots, True, config.PURPLE)
        dots_rect = dots_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(dots_text, dots_rect)
        
        # Progress bar (1970s style)
        if self.start_time:
            progress = min((time.time() - self.start_time) / self.loading_duration, 1.0)
            bar_width = 400
            bar_height = 25
            bar_x = (config.SCREEN_WIDTH - bar_width) // 2
            bar_y = config.SCREEN_HEIGHT // 2 + 80
            
            # Draw bar background with black border
            pygame.draw.rect(self.screen, config.BLACK, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, config.PURPLE, (bar_x, bar_y, bar_width, bar_height), 3)
            
            # Draw progress fill in purple
            fill_width = int(bar_width * progress)
            if fill_width > 0:
                pygame.draw.rect(self.screen, config.PURPLE, 
                               (bar_x + 3, bar_y + 3, fill_width - 6, bar_height - 6))
                # Add inner highlight
                if fill_width > 6:
                    pygame.draw.rect(self.screen, (180, 50, 255), 
                                   (bar_x + 3, bar_y + 3, fill_width - 6, 5))
        
        pygame.display.flip()

