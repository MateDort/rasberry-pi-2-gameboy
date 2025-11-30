"""
1970s-style lobby screen for game selection
"""
import pygame
import config

class Lobby:
    def __init__(self, screen):
        self.screen = screen
        self.selected_index = 0
        self.games = ["SNAKE"]
        self.font_large = None
        self.font_medium = None
        self.clock = pygame.time.Clock()
        
    def initialize_fonts(self):
        """Initialize fonts for the lobby"""
        try:
            # Try to use a retro-style font, fallback to default
            self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        except:
            self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.games)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.games)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return "start_game"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check if click is on a game item
                start_y = config.SCREEN_HEIGHT // 2 - 50
                for i, game in enumerate(self.games):
                    y_pos = start_y + i * 80
                    if y_pos <= mouse_pos[1] <= y_pos + 60:
                        self.selected_index = i
                        return "start_game"
        return None
    
    def draw(self):
        """Draw the lobby screen"""
        # 1970s retro background - gradient effect
        for y in range(config.SCREEN_HEIGHT):
            # Create a gradient from brown to beige
            ratio = y / config.SCREEN_HEIGHT
            r = int(config.RETRO_BROWN[0] * (1 - ratio) + config.RETRO_BEIGE[0] * ratio)
            g = int(config.RETRO_BROWN[1] * (1 - ratio) + config.RETRO_BEIGE[1] * ratio)
            b = int(config.RETRO_BROWN[2] * (1 - ratio) + config.RETRO_BEIGE[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (config.SCREEN_WIDTH, y))
        
        # Title
        if self.font_large is None:
            self.initialize_fonts()
        
        title_text = self.font_large.render("GAME BOY", True, config.RETRO_ORANGE)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Select a Game", True, config.RETRO_YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Game list
        start_y = config.SCREEN_HEIGHT // 2 - 50
        for i, game in enumerate(self.games):
            y_pos = start_y + i * 80
            
            # Highlight selected game
            if i == self.selected_index:
                # Draw selection box
                box_rect = pygame.Rect(
                    config.SCREEN_WIDTH // 2 - 150,
                    y_pos - 10,
                    300,
                    60
                )
                pygame.draw.rect(self.screen, config.RETRO_ORANGE, box_rect, 3)
                color = config.RETRO_YELLOW
            else:
                color = config.RETRO_BEIGE
            
            # Draw game name
            game_text = self.font_medium.render(game, True, color)
            game_rect = game_text.get_rect(center=(config.SCREEN_WIDTH // 2, y_pos + 20))
            self.screen.blit(game_text, game_rect)
        
        # Instructions
        instruction_text = self.font_medium.render("Press ENTER or Click to Start", True, config.WHITE)
        instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 100))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

