"""
Snake game implementation
"""
import pygame
import random
import config
import high_score

class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()
        self.font_medium = None
        self.font_small = None
        self.clock = pygame.time.Clock()
        self.frame_count = 0
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Snake starts with length 1 at center
        center_x = config.GRID_WIDTH // 2
        center_y = config.GRID_HEIGHT // 2
        self.snake = [(center_x, center_y)]
        self.direction = (1, 0)  # Moving right initially
        self.next_direction = (1, 0)
        self.apple = self.generate_apple()
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        
    def generate_apple(self):
        """Generate a new apple position that's not on the snake"""
        while True:
            x = random.randint(0, config.GRID_WIDTH - 1)
            y = random.randint(0, config.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.frame_count += 1
        
        # Move snake at specified speed
        if self.frame_count % config.SNAKE_SPEED == 0:
            self.direction = self.next_direction
            
            # Calculate new head position
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= config.GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= config.GRID_HEIGHT):
                self.game_over = True
                # Update high score
                high_score.update_high_score(self.score)
                return
            
            # Check self collision
            if new_head in self.snake:
                self.game_over = True
                high_score.update_high_score(self.score)
                return
            
            # Add new head
            self.snake.insert(0, new_head)
            
            # Check if apple eaten
            if new_head == self.apple:
                self.score += 1
                self.apple = self.generate_apple()
            else:
                # Remove tail if no apple eaten
                self.snake.pop()
    
    def draw(self):
        """Draw the game"""
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Draw background
        self.screen.fill(config.DARK_GREEN)
        
        # Draw score and high score at top
        score_text = self.font_small.render(f"Score: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        current_high = high_score.load_high_score()
        high_score_text = self.font_small.render(f"High Score: {current_high}", True, config.WHITE)
        high_score_rect = high_score_text.get_rect()
        high_score_rect.topright = (config.SCREEN_WIDTH - 10, 10)
        self.screen.blit(high_score_text, high_score_rect)
        
        # Draw snake
        for segment in self.snake:
            x = segment[0] * config.GRID_SIZE
            y = segment[1] * config.GRID_SIZE
            pygame.draw.rect(self.screen, config.PURPLE, 
                           (x, y, config.GRID_SIZE, config.GRID_SIZE))
            # Add border for better visibility
            pygame.draw.rect(self.screen, (100, 0, 200), 
                           (x, y, config.GRID_SIZE, config.GRID_SIZE), 1)
        
        # Draw apple (emoji)
        apple_x = self.apple[0] * config.GRID_SIZE
        apple_y = self.apple[1] * config.GRID_SIZE
        
        # Try to render apple emoji, fallback to drawing a red circle
        try:
            # Try using system font that might support emojis
            import sys
            if sys.platform == "darwin":  # macOS
                apple_font = pygame.font.SysFont("Apple Color Emoji", config.GRID_SIZE)
            elif sys.platform.startswith("linux"):
                apple_font = pygame.font.SysFont("Noto Color Emoji", config.GRID_SIZE)
            else:
                apple_font = pygame.font.Font(None, config.GRID_SIZE)
            
            apple_surface = apple_font.render("🍎", True, (255, 0, 0))
            if apple_surface.get_width() > 0:  # Check if emoji rendered
                apple_surface = pygame.transform.scale(apple_surface, (config.GRID_SIZE, config.GRID_SIZE))
                self.screen.blit(apple_surface, (apple_x, apple_y))
            else:
                raise Exception("Emoji not supported")
        except:
            # Fallback: draw a red circle (apple shape)
            center_x = apple_x + config.GRID_SIZE // 2
            center_y = apple_y + config.GRID_SIZE // 2
            radius = config.GRID_SIZE // 2 - 2
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), radius)
            # Draw a small green stem
            pygame.draw.rect(self.screen, (0, 150, 0), 
                           (center_x - 2, apple_y + 2, 4, 6))
        
        pygame.display.flip()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over

