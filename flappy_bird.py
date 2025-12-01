"""
Flappy Bird game implementation
"""
import pygame
import random
import config
import high_score

class FlappyBird:
    def __init__(self, screen):
        self.screen = screen
        self.bird_image = None
        self.load_bird_sprite()
        self.reset_game()
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.clock = pygame.time.Clock()
        self.frame_count = 0
    
    def load_bird_sprite(self):
        """Load the bird sprite image"""
        try:
            self.bird_image = pygame.image.load("characters/flappy_bird_bird.png").convert_alpha()
            # Get the actual size of the sprite
            original_width = self.bird_image.get_width()
            original_height = self.bird_image.get_height()
            
            # Scale down if sprite is too large (max 60x60 pixels)
            max_size = 60
            if original_width > max_size or original_height > max_size:
                scale_factor = min(max_size / original_width, max_size / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                self.bird_image = pygame.transform.scale(self.bird_image, (new_width, new_height))
                self.bird_width = new_width
                self.bird_height = new_height
            else:
                self.bird_width = original_width
                self.bird_height = original_height
        except pygame.error as e:
            print(f"Error loading bird sprite: {e}")
            # Fallback to a default size if image can't be loaded
            self.bird_width = 30
            self.bird_height = 30
            self.bird_image = None
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Bird properties - ensure safe starting position
        self.bird_x = config.SCREEN_WIDTH // 4
        # Start bird higher up to account for sprite size, ensure it's well above ground
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        safe_start_y = ground_y - 100  # Start 100 pixels above ground
        self.bird_y = max(safe_start_y, config.SCREEN_HEIGHT // 2)
        self.bird_velocity = 0
        
        # Game state
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        
        # Pipes
        self.pipes = []
        self.pipe_width = 60
        self.pipe_gap = 180
        self.pipe_speed = 3
        self.pipe_spawn_timer = 0
        self.pipe_spawn_interval = 120  # Frames between pipe spawns
        
        # Background scrolling
        self.ground_scroll = 0
        self.city_scroll = 0
        
        # Generate initial pipes
        self.spawn_pipe()
    
    def spawn_pipe(self):
        """Spawn a new pipe pair"""
        gap_y = random.randint(150, config.SCREEN_HEIGHT - config.GROUND_HEIGHT - 150)
        top_pipe_height = gap_y - self.pipe_gap // 2
        bottom_pipe_y = gap_y + self.pipe_gap // 2
        bottom_pipe_height = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - bottom_pipe_y
        
        self.pipes.append({
            'x': config.SCREEN_WIDTH,
            'top_height': top_pipe_height,
            'bottom_y': bottom_pipe_y,
            'bottom_height': bottom_pipe_height,
            'passed': False
        })
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not self.game_over:
                # Jump/flap
                self.bird_velocity = -config.BIRD_JUMP_STRENGTH
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.game_over:  # Left click
                # Jump/flap
                self.bird_velocity = -config.BIRD_JUMP_STRENGTH
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.frame_count += 1
        
        # Update bird physics
        self.bird_velocity += config.GRAVITY
        self.bird_y += self.bird_velocity
        
        # Update pipes
        for pipe in self.pipes:
            pipe['x'] -= self.pipe_speed
            
            # Check if bird passed the pipe (using bird's left edge)
            bird_left_edge = self.bird_x - self.bird_width // 2
            if not pipe['passed'] and pipe['x'] + self.pipe_width < bird_left_edge:
                pipe['passed'] = True
                self.score += 1
        
        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p['x'] + self.pipe_width > 0]
        
        # Spawn new pipes
        self.pipe_spawn_timer += 1
        if self.pipe_spawn_timer >= self.pipe_spawn_interval:
            self.spawn_pipe()
            self.pipe_spawn_timer = 0
        
        # Update background scrolling
        self.ground_scroll = (self.ground_scroll - self.pipe_speed) % config.GROUND_PATTERN_WIDTH
        self.city_scroll = (self.city_scroll - self.pipe_speed * 0.3) % config.SCREEN_WIDTH
        
        # Check collisions
        self.check_collisions()
    
    def check_collisions(self):
        """Check for collisions with pipes and ground"""
        # Use a smaller collision box than the full sprite for more forgiving gameplay
        # Scale down collision box to 70% of sprite size
        collision_width = int(self.bird_width * 0.7)
        collision_height = int(self.bird_height * 0.7)
        
        # Ground collision - check bottom edge of collision box
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        bird_bottom = self.bird_y + collision_height // 2
        if bird_bottom >= ground_y:
            self.game_over = True
            high_score.update_high_score(self.score, "flappy_bird")
            return
        
        # Ceiling collision - check top edge of collision box
        bird_top = self.bird_y - collision_height // 2
        if bird_top <= 0:
            self.game_over = True
            high_score.update_high_score(self.score, "flappy_bird")
            return
        
        # Pipe collisions - use smaller collision box
        bird_rect = pygame.Rect(
            self.bird_x - collision_width // 2,
            self.bird_y - collision_height // 2,
            collision_width,
            collision_height
        )
        
        for pipe in self.pipes:
            # Top pipe
            top_pipe_rect = pygame.Rect(
                pipe['x'],
                0,
                self.pipe_width,
                pipe['top_height']
            )
            
            # Bottom pipe
            bottom_pipe_rect = pygame.Rect(
                pipe['x'],
                pipe['bottom_y'],
                self.pipe_width,
                pipe['bottom_height']
            )
            
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                self.game_over = True
                high_score.update_high_score(self.score, "flappy_bird")
                return
    
    def draw_bird(self):
        """Draw the bird using the sprite image"""
        if self.bird_image:
            # Calculate position to center the sprite at bird_x, bird_y
            bird_rect = self.bird_image.get_rect()
            bird_rect.center = (int(self.bird_x), int(self.bird_y))
            self.screen.blit(self.bird_image, bird_rect)
        else:
            # Fallback if sprite couldn't be loaded
            pygame.draw.circle(self.screen, config.BIRD_YELLOW, (int(self.bird_x), int(self.bird_y)), 15)
    
    def draw_pipe(self, x, height, is_top):
        """Draw a pipe"""
        if is_top:
            # Top pipe (extends downward)
            pipe_rect = pygame.Rect(x, 0, self.pipe_width, height)
        else:
            # Bottom pipe (extends upward)
            pipe_rect = pygame.Rect(x, config.SCREEN_HEIGHT - config.GROUND_HEIGHT - height, self.pipe_width, height)
        
        # Main pipe body (green)
        pygame.draw.rect(self.screen, config.PIPE_GREEN, pipe_rect)
        
        # Darker green outline
        pygame.draw.rect(self.screen, config.PIPE_DARK_GREEN, pipe_rect, 3)
        
        # Lighter green highlight on left side
        highlight_rect = pygame.Rect(x + 2, pipe_rect.y + 2, 8, pipe_rect.height - 4)
        if is_top:
            highlight_rect.y = pipe_rect.y + 2
        else:
            highlight_rect.y = pipe_rect.y + 2
        pygame.draw.rect(self.screen, config.PIPE_LIGHT_GREEN, highlight_rect)
        
        # Pipe rim (wider at ends)
        rim_width = self.pipe_width + 8
        rim_height = 20
        if is_top:
            rim_rect = pygame.Rect(x - 4, height - rim_height, rim_width, rim_height)
        else:
            rim_rect = pygame.Rect(x - 4, config.SCREEN_HEIGHT - config.GROUND_HEIGHT - height, rim_width, rim_height)
        
        pygame.draw.rect(self.screen, config.PIPE_GREEN, rim_rect)
        pygame.draw.rect(self.screen, config.PIPE_DARK_GREEN, rim_rect, 3)
    
    def draw_background(self):
        """Draw the background (sky, clouds, city)"""
        # Sky (light blue)
        self.screen.fill(config.SKY_BLUE)
        
        # Clouds (white, pixelated)
        cloud_positions = [
            (100, 80), (250, 120), (400, 100), (550, 90), (700, 110),
            (150, 200), (350, 180), (500, 200), (650, 190)
        ]
        for x, y in cloud_positions:
            # Scroll clouds slightly
            cloud_x = (x - self.city_scroll * 0.2) % (config.SCREEN_WIDTH + 100) - 50
            # Simple cloud shape (pixelated)
            pygame.draw.circle(self.screen, config.WHITE, (int(cloud_x), y), 15)
            pygame.draw.circle(self.screen, config.WHITE, (int(cloud_x) + 10, y), 12)
            pygame.draw.circle(self.screen, config.WHITE, (int(cloud_x) + 20, y), 15)
            pygame.draw.circle(self.screen, config.WHITE, (int(cloud_x) + 5, y - 8), 10)
            pygame.draw.circle(self.screen, config.WHITE, (int(cloud_x) + 15, y - 8), 10)
        
        # City skyline (light blue silhouette)
        city_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - 80
        city_buildings = [
            (0, 40), (50, 60), (100, 35), (150, 55), (200, 45),
            (250, 65), (300, 50), (350, 70), (400, 40), (450, 60),
            (500, 55), (550, 45), (600, 65), (650, 50), (700, 60), (750, 40)
        ]
        for i, (base_x, height) in enumerate(city_buildings):
            city_x = (base_x - self.city_scroll) % (config.SCREEN_WIDTH + 100) - 50
            # Building rectangle
            building_rect = pygame.Rect(
                int(city_x),
                city_y - height,
                30,
                height
            )
            pygame.draw.rect(self.screen, config.CITY_BLUE, building_rect)
            # Add some windows (darker blue)
            if height > 20:
                for wy in range(city_y - height + 10, city_y - 5, 15):
                    for wx in range(int(city_x) + 5, int(city_x) + 25, 10):
                        pygame.draw.rect(self.screen, config.CITY_DARK_BLUE, (wx, wy, 4, 6))
        
        # Ground/horizon line (darker green strip)
        horizon_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - 5
        pygame.draw.rect(self.screen, config.HORIZON_GREEN, 
                        (0, horizon_y, config.SCREEN_WIDTH, 5))
    
    def draw_ground(self):
        """Draw the ground"""
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        
        # Main ground (light brown)
        ground_rect = pygame.Rect(0, ground_y, config.SCREEN_WIDTH, config.GROUND_HEIGHT)
        self.screen.fill(config.GROUND_BROWN, ground_rect)
        
        # Scrolling ground pattern (striped green border)
        pattern_width = config.GROUND_PATTERN_WIDTH
        for x in range(-pattern_width, config.SCREEN_WIDTH + pattern_width, pattern_width):
            pattern_x = (x + self.ground_scroll) % (pattern_width * 2) - pattern_width
            
            # Green and darker green stripes
            for i in range(0, pattern_width, 20):
                stripe_x = pattern_x + i
                if 0 <= stripe_x < config.SCREEN_WIDTH:
                    color = config.GROUND_GREEN if (i // 20) % 2 == 0 else config.GROUND_DARK_GREEN
                    pygame.draw.rect(self.screen, color, 
                                   (stripe_x, ground_y, 20, 5))
    
    def draw(self):
        """Draw the game"""
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Draw background
        self.draw_background()
        
        # Draw pipes
        for pipe in self.pipes:
            self.draw_pipe(pipe['x'], pipe['top_height'], True)
            self.draw_pipe(pipe['x'], pipe['bottom_height'], False)
        
        # Draw ground
        self.draw_ground()
        
        # Draw bird
        if not self.game_over:
            self.draw_bird()
        
        # Draw score (upper right)
        score_text = self.font_medium.render(str(self.score), True, config.WHITE)
        score_rect = score_text.get_rect()
        score_rect.topright = (config.SCREEN_WIDTH - 10, 10)
        self.screen.blit(score_text, score_rect)
        
        pygame.display.flip()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over

