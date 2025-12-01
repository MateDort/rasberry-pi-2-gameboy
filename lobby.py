"""
1970s-style lobby screen for game selection
"""
import pygame
import config

class Lobby:
    def __init__(self, screen):
        self.screen = screen
        self.selected_index = 0
        self.games = ["SNAKE", "FLAPPY BIRD", "SUDOKU"]
        self.font_large = None
        self.font_medium = None
        self.clock = pygame.time.Clock()
        self.scroll_offset = 0  # Track how many items are scrolled up
        self.item_height = 100  # Height of each menu item
        self.item_spacing = 100  # Spacing between items
        
    def initialize_fonts(self):
        """Initialize fonts for the lobby"""
        try:
            # Try to use a retro-style font, fallback to default
            self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        except:
            self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
    
    def get_visible_range(self):
        """Calculate which items are visible on screen"""
        # Calculate available space for menu items
        # Title area: ~180px, instructions area: ~80px
        available_height = config.SCREEN_HEIGHT - 180 - 80
        max_visible = available_height // self.item_spacing
        
        # Calculate visible range
        visible_start = self.scroll_offset
        visible_end = min(self.scroll_offset + max_visible, len(self.games))
        
        return visible_start, visible_end, max_visible
    
    def ensure_selection_visible(self):
        """Ensure the selected item is visible, adjusting scroll if needed"""
        visible_start, visible_end, max_visible = self.get_visible_range()
        
        # If selected item is above visible range, scroll up
        if self.selected_index < visible_start:
            self.scroll_offset = self.selected_index
        
        # If selected item is below visible range, scroll down
        elif self.selected_index >= visible_end:
            self.scroll_offset = max(0, self.selected_index - max_visible + 1)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
                self.ensure_selection_visible()
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.games) - 1, self.selected_index + 1)
                self.ensure_selection_visible()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                game_name = self.games[self.selected_index].lower().replace(" ", "_")
                return f"start_game:{game_name}"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check if click is on a game item
                visible_start, visible_end, _ = self.get_visible_range()
                start_y = config.SCREEN_HEIGHT // 2 - 30
                
                for i in range(visible_start, visible_end):
                    relative_index = i - visible_start
                    y_pos = start_y + relative_index * self.item_spacing
                    if y_pos <= mouse_pos[1] <= y_pos + 70:
                        self.selected_index = i
                        game_name = self.games[i].lower().replace(" ", "_")
                        return f"start_game:{game_name}"
        elif event.type == pygame.MOUSEWHEEL:
            # Handle mouse wheel scrolling
            if event.y > 0:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
                if self.selected_index > 0:
                    self.selected_index -= 1
            elif event.y < 0:  # Scroll down
                visible_start, visible_end, max_visible = self.get_visible_range()
                if visible_end < len(self.games):
                    self.scroll_offset = min(len(self.games) - max_visible, self.scroll_offset + 1)
                if self.selected_index < len(self.games) - 1:
                    self.selected_index += 1
            self.ensure_selection_visible()
        return None
    
    def draw(self):
        """Draw the lobby screen"""
        # 1970s retro background - dark green with pattern
        self.screen.fill(config.DARK_GREEN)
        
        # Add some 1970s style pattern elements
        # Draw diagonal lines for retro effect
        for i in range(0, config.SCREEN_WIDTH + config.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 60, 35), 
                           (i, 0), (i - config.SCREEN_HEIGHT, config.SCREEN_HEIGHT), 1)
        
        # Draw decorative borders
        pygame.draw.rect(self.screen, config.BLACK, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 8)
        pygame.draw.rect(self.screen, config.PURPLE, (10, 10, config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 20), 3)
        
        # Title
        if self.font_large is None:
            self.initialize_fonts()
        
        # Title with 1970s style - outlined text
        title_text = self.font_large.render("GAME BOY", True, config.PURPLE)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        # Draw black outline
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    outline_rect = title_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_text = self.font_large.render("GAME BOY", True, config.BLACK)
                    self.screen.blit(outline_text, outline_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("SELECT A GAME", True, config.PURPLE)
        subtitle_rect = subtitle_text.get_rect(center=(config.SCREEN_WIDTH // 2, 160))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Decorative line under subtitle
        pygame.draw.line(self.screen, config.PURPLE, 
                        (config.SCREEN_WIDTH // 2 - 150, 180), 
                        (config.SCREEN_WIDTH // 2 + 150, 180), 2)
        
        # Get visible range
        visible_start, visible_end, _ = self.get_visible_range()
        
        # Game list - only draw visible items
        start_y = config.SCREEN_HEIGHT // 2 - 30
        for i in range(visible_start, visible_end):
            relative_index = i - visible_start
            y_pos = start_y + relative_index * self.item_spacing
            game = self.games[i]
            
            # Highlight selected game with 1970s style box
            if i == self.selected_index:
                # Draw selection box with retro style
                box_rect = pygame.Rect(
                    config.SCREEN_WIDTH // 2 - 180,
                    y_pos - 15,
                    360,
                    70
                )
                # Purple background for selected
                pygame.draw.rect(self.screen, config.PURPLE, box_rect)
                pygame.draw.rect(self.screen, config.BLACK, box_rect, 4)
                # Inner highlight
                pygame.draw.rect(self.screen, (180, 50, 255), 
                               (box_rect.x + 4, box_rect.y + 4, box_rect.width - 8, box_rect.height - 8), 2)
                color = config.BLACK
            else:
                color = config.PURPLE
            
            # Draw game name
            game_text = self.font_medium.render(game, True, color)
            game_rect = game_text.get_rect(center=(config.SCREEN_WIDTH // 2, y_pos + 20))
            self.screen.blit(game_text, game_rect)
        
        # Draw scroll indicators
        if visible_start > 0:
            # Show up arrow
            arrow_y = start_y - 30
            arrow_points = [
                (config.SCREEN_WIDTH // 2 - 10, arrow_y),
                (config.SCREEN_WIDTH // 2, arrow_y - 15),
                (config.SCREEN_WIDTH // 2 + 10, arrow_y)
            ]
            pygame.draw.polygon(self.screen, config.PURPLE, arrow_points)
        
        if visible_end < len(self.games):
            # Show down arrow
            arrow_y = start_y + (visible_end - visible_start) * self.item_spacing + 30
            arrow_points = [
                (config.SCREEN_WIDTH // 2 - 10, arrow_y),
                (config.SCREEN_WIDTH // 2, arrow_y + 15),
                (config.SCREEN_WIDTH // 2 + 10, arrow_y)
            ]
            pygame.draw.polygon(self.screen, config.PURPLE, arrow_points)
        
        # Instructions at bottom
        instruction_y = config.SCREEN_HEIGHT - 80
        pygame.draw.line(self.screen, config.PURPLE, 
                        (config.SCREEN_WIDTH // 2 - 200, instruction_y - 20), 
                        (config.SCREEN_WIDTH // 2 + 200, instruction_y - 20), 2)
        instruction_text = self.font_medium.render("PRESS ENTER OR CLICK TO START", True, config.PURPLE)
        instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH // 2, instruction_y))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()

