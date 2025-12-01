"""
Game Over screen with score display and restart options
"""
import pygame
import config
import high_score

class GameOver:
    def __init__(self, screen, final_score, game_name="snake"):
        self.screen = screen
        self.final_score = final_score
        self.game_name = game_name
        self.high_score = high_score.load_high_score(game_name)
        self.new_high_score = final_score > self.high_score
        if self.new_high_score:
            self.high_score = final_score
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.restart_button = None
        self.lobby_button = None
        self.selected_button = 0  # 0 = restart, 1 = lobby
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.selected_button = 1 - self.selected_button
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_button == 0:
                    return "restart_game"
                else:
                    return "return_lobby"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check restart button
                if self.restart_button and self.restart_button.collidepoint(mouse_pos):
                    return "restart_game"
                # Check lobby button
                if self.lobby_button and self.lobby_button.collidepoint(mouse_pos):
                    return "return_lobby"
        elif event.type == pygame.MOUSEMOTION:
            # Update selected button based on mouse hover
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button and self.restart_button.collidepoint(mouse_pos):
                self.selected_button = 0
            elif self.lobby_button and self.lobby_button.collidepoint(mouse_pos):
                self.selected_button = 1
        return None
    
    def draw(self):
        """Draw the game over screen"""
        if self.font_large is None:
            self.initialize_fonts()
        
        # 1970s style background - dark green with black border
        self.screen.fill(config.DARK_GREEN)
        
        # Add decorative pattern
        for i in range(0, config.SCREEN_WIDTH + config.SCREEN_HEIGHT, 30):
            pygame.draw.line(self.screen, (20, 60, 35), 
                           (i, 0), (i - config.SCREEN_HEIGHT, config.SCREEN_HEIGHT), 1)
        
        # Draw borders
        pygame.draw.rect(self.screen, config.BLACK, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 10)
        pygame.draw.rect(self.screen, config.PURPLE, (15, 15, config.SCREEN_WIDTH - 30, config.SCREEN_HEIGHT - 30), 4)
        
        # Game Over text with 1970s style - outlined
        game_over_text = self.font_large.render("GAME OVER", True, config.PURPLE)
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, 120))
        # Draw black outline
        for dx in [-3, -2, -1, 0, 1, 2, 3]:
            for dy in [-3, -2, -1, 0, 1, 2, 3]:
                if dx != 0 or dy != 0:
                    outline_rect = game_over_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_text = self.font_large.render("GAME OVER", True, config.BLACK)
                    self.screen.blit(outline_text, outline_rect)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Decorative line
        pygame.draw.line(self.screen, config.PURPLE, 
                        (config.SCREEN_WIDTH // 2 - 200, 160), 
                        (config.SCREEN_WIDTH // 2 + 200, 160), 3)
        
        # Score display
        score_y = 220
        score_text = self.font_medium.render(f"SCORE: {self.final_score}", True, config.PURPLE)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, score_y))
        self.screen.blit(score_text, score_rect)
        
        # High score display
        high_score_y = score_y + 60
        if self.new_high_score:
            high_score_text = self.font_medium.render(f"NEW HIGH SCORE: {self.high_score}!", True, config.PURPLE)
            # Add black outline for emphasis
            outline_rect = high_score_text.get_rect(center=(config.SCREEN_WIDTH // 2, high_score_y))
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    if dx != 0 or dy != 0:
                        outline_pos = outline_rect.copy()
                        outline_pos.x += dx
                        outline_pos.y += dy
                        outline = self.font_medium.render(f"NEW HIGH SCORE: {self.high_score}!", True, config.BLACK)
                        self.screen.blit(outline, outline_pos)
        else:
            high_score_text = self.font_medium.render(f"HIGH SCORE: {self.high_score}", True, config.PURPLE)
        high_score_rect = high_score_text.get_rect(center=(config.SCREEN_WIDTH // 2, high_score_y))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Buttons with 1970s style
        button_y = high_score_y + 100
        button_width = 220
        button_height = 55
        button_spacing = 40
        
        # Restart button
        restart_x = config.SCREEN_WIDTH // 2 - button_width - button_spacing // 2
        self.restart_button = pygame.Rect(restart_x, button_y, button_width, button_height)
        if self.selected_button == 0:
            # Selected - purple background
            pygame.draw.rect(self.screen, config.PURPLE, self.restart_button)
            pygame.draw.rect(self.screen, config.BLACK, self.restart_button, 4)
            pygame.draw.rect(self.screen, (180, 50, 255), 
                           (self.restart_button.x + 3, self.restart_button.y + 3, 
                            self.restart_button.width - 6, self.restart_button.height - 6), 2)
            text_color = config.BLACK
        else:
            # Not selected - black border on dark green
            pygame.draw.rect(self.screen, config.DARK_GREEN, self.restart_button)
            pygame.draw.rect(self.screen, config.PURPLE, self.restart_button, 4)
            text_color = config.PURPLE
        restart_text = self.font_small.render("RESTART GAME", True, text_color)
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)
        
        # Return to Lobby button
        lobby_x = config.SCREEN_WIDTH // 2 + button_spacing // 2
        self.lobby_button = pygame.Rect(lobby_x, button_y, button_width, button_height)
        if self.selected_button == 1:
            # Selected - purple background
            pygame.draw.rect(self.screen, config.PURPLE, self.lobby_button)
            pygame.draw.rect(self.screen, config.BLACK, self.lobby_button, 4)
            pygame.draw.rect(self.screen, (180, 50, 255), 
                           (self.lobby_button.x + 3, self.lobby_button.y + 3, 
                            self.lobby_button.width - 6, self.lobby_button.height - 6), 2)
            text_color = config.BLACK
        else:
            # Not selected - black border on dark green
            pygame.draw.rect(self.screen, config.DARK_GREEN, self.lobby_button)
            pygame.draw.rect(self.screen, config.PURPLE, self.lobby_button, 4)
            text_color = config.PURPLE
        lobby_text = self.font_small.render("RETURN TO LOBBY", True, text_color)
        lobby_text_rect = lobby_text.get_rect(center=self.lobby_button.center)
        self.screen.blit(lobby_text, lobby_text_rect)
        
        pygame.display.flip()

