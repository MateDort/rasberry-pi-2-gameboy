"""
Game Over screen with score display and restart options
"""
import pygame
import config
import high_score

class GameOver:
    def __init__(self, screen, final_score):
        self.screen = screen
        self.final_score = final_score
        self.high_score = high_score.load_high_score()
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
        
        # Dark background
        self.screen.fill(config.BLACK)
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, config.RETRO_ORANGE)
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score display
        score_y = 250
        score_text = self.font_medium.render(f"Score: {self.final_score}", True, config.WHITE)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, score_y))
        self.screen.blit(score_text, score_rect)
        
        # High score display
        high_score_y = score_y + 50
        if self.new_high_score:
            high_score_text = self.font_medium.render(f"NEW HIGH SCORE: {self.high_score}!", True, config.RETRO_YELLOW)
        else:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, config.WHITE)
        high_score_rect = high_score_text.get_rect(center=(config.SCREEN_WIDTH // 2, high_score_y))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Buttons
        button_y = high_score_y + 100
        button_width = 200
        button_height = 50
        button_spacing = 50
        
        # Restart button
        restart_x = config.SCREEN_WIDTH // 2 - button_width - button_spacing // 2
        self.restart_button = pygame.Rect(restart_x, button_y, button_width, button_height)
        restart_color = config.RETRO_YELLOW if self.selected_button == 0 else config.RETRO_ORANGE
        pygame.draw.rect(self.screen, restart_color, self.restart_button)
        pygame.draw.rect(self.screen, config.WHITE, self.restart_button, 2)
        restart_text = self.font_small.render("Restart Game", True, config.BLACK)
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)
        
        # Return to Lobby button
        lobby_x = config.SCREEN_WIDTH // 2 + button_spacing // 2
        self.lobby_button = pygame.Rect(lobby_x, button_y, button_width, button_height)
        lobby_color = config.RETRO_YELLOW if self.selected_button == 1 else config.RETRO_ORANGE
        pygame.draw.rect(self.screen, lobby_color, self.lobby_button)
        pygame.draw.rect(self.screen, config.WHITE, self.lobby_button, 2)
        lobby_text = self.font_small.render("Return to Lobby", True, config.BLACK)
        lobby_text_rect = lobby_text.get_rect(center=self.lobby_button.center)
        self.screen.blit(lobby_text, lobby_text_rect)
        
        pygame.display.flip()

