"""
Super Mario platformer game implementation
"""
import pygame
import config
import high_score
from mario_sprites import MarioSprites

class MarioGame:
    def __init__(self, screen):
        self.screen = screen
        self.sprites = MarioSprites()
        self.sprites.scale_factor = config.MARIO_SPRITE_SCALE
        self.sprites.load_all()
        
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.clock = pygame.time.Clock()
        self.frame_count = 0
        
        self.reset_game()
    
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Mario properties
        self.mario_x = 100
        self.mario_y = 400
        self.mario_velocity_x = 0
        self.mario_velocity_y = 0
        self.mario_facing_right = True
        self.mario_on_ground = False
        self.mario_animation_frame = 0
        self.mario_animation_timer = 0
        
        # Game state
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        self.camera_x = 0
        
        # Level data (simple 2D array representation)
        self.level_width = config.MARIO_LEVEL_WIDTH
        self.level_height = config.MARIO_LEVEL_HEIGHT
        self.level_data = self.create_level()
        
        # Ensure level_data is valid
        if not self.level_data or len(self.level_data) == 0:
            # Create a minimal level if creation failed
            tile_size = config.MARIO_SCALED_TILE_SIZE
            width_tiles = max(10, self.level_width // tile_size)
            height_tiles = max(10, self.level_height // tile_size)
            self.level_data = [[0] * width_tiles for _ in range(height_tiles)]
            # Add ground
            ground_y = height_tiles - 1
            for x in range(width_tiles):
                self.level_data[ground_y][x] = 1
        
        # Enemies
        self.enemies = []
        self.spawn_initial_enemies()
        
        # Items (coins, power-ups)
        self.items = []
        self.spawn_initial_items()
        
        # Keys pressed
        self.keys_pressed = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_SPACE: False,
            pygame.K_LSHIFT: False,
            pygame.K_RSHIFT: False
        }
    
    def create_level(self):
        """Create a simple level layout"""
        # Create a 2D grid representing the level
        # 0 = empty, 1 = ground, 2 = brick, 3 = question block
        level = []
        tile_size = config.MARIO_SCALED_TILE_SIZE
        width_tiles = self.level_width // tile_size
        height_tiles = self.level_height // tile_size
        
        # Ensure minimum dimensions
        if width_tiles < 10:
            width_tiles = 10
        if height_tiles < 10:
            height_tiles = 10
        
        # Initialize with empty space
        for y in range(height_tiles):
            level.append([0] * width_tiles)
        
        # Add ground platform at bottom
        ground_y = height_tiles - 3
        # Ensure ground_y is valid
        if ground_y < 0:
            ground_y = height_tiles - 1
        
        for x in range(width_tiles):
            level[ground_y][x] = 1  # Ground
            if x % 2 == 0 and ground_y > 0:
                level[ground_y - 1][x] = 1  # Some ground tiles
        
        # Add some platforms (ensure indices are within bounds)
        # Platform 1
        platform1_y = max(0, ground_y - 5)
        for x in range(min(20, width_tiles), min(30, width_tiles)):
            if x < width_tiles:
                level[platform1_y][x] = 1
        
        # Platform 2
        platform2_y = max(0, ground_y - 8)
        for x in range(min(40, width_tiles), min(50, width_tiles)):
            if x < width_tiles:
                level[platform2_y][x] = 1
        
        # Platform 3
        platform3_y = max(0, ground_y - 6)
        for x in range(min(60, width_tiles), min(75, width_tiles)):
            if x < width_tiles:
                level[platform3_y][x] = 1
        
        # Add some bricks
        brick1_y = max(0, ground_y - 4)
        for x in range(min(15, width_tiles), min(18, width_tiles)):
            if x < width_tiles:
                level[brick1_y][x] = 2
        
        brick2_y = max(0, ground_y - 9)
        for x in range(min(35, width_tiles), min(38, width_tiles)):
            if x < width_tiles:
                level[brick2_y][x] = 2
        
        # Add question blocks (ensure indices are within bounds)
        qblock1_y = max(0, ground_y - 5)
        qblock1_x = min(25, width_tiles - 1)
        if qblock1_x >= 0 and qblock1_y >= 0:
            level[qblock1_y][qblock1_x] = 3
        
        qblock2_y = max(0, ground_y - 9)
        qblock2_x = min(45, width_tiles - 1)
        if qblock2_x >= 0 and qblock2_y >= 0:
            level[qblock2_y][qblock2_x] = 3
        
        return level
    
    def spawn_initial_enemies(self):
        """Spawn initial enemies in the level"""
        self.enemies = []
        if not self.level_data or len(self.level_data) == 0:
            return
        
        tile_size = config.MARIO_SCALED_TILE_SIZE
        ground_y = (len(self.level_data) - 3) * tile_size
        
        # Spawn a few Koopas
        enemy_positions = [
            (400, ground_y - tile_size),
            (600, ground_y - tile_size),
            (900, ground_y - tile_size),
            (1200, ground_y - tile_size)
        ]
        
        for x, y in enemy_positions:
            self.enemies.append({
                'x': x,
                'y': y,
                'velocity_x': -config.KOOPA_SPEED,
                'facing_right': False,
                'animation_frame': 0,
                'animation_timer': 0,
                'type': 'koopa',
                'alive': True
            })
    
    def spawn_initial_items(self):
        """Spawn initial items (coins, power-ups)"""
        self.items = []
        if not self.level_data or len(self.level_data) == 0:
            return
        
        tile_size = config.MARIO_SCALED_TILE_SIZE
        ground_y = (len(self.level_data) - 3) * tile_size
        
        # Spawn coins
        coin_positions = [
            (300, ground_y - tile_size * 2),
            (500, ground_y - tile_size * 2),
            (700, ground_y - tile_size * 2),
            (800, ground_y - tile_size * 5),
            (1000, ground_y - tile_size * 7),
            (1100, ground_y - tile_size * 2)
        ]
        
        for x, y in coin_positions:
            self.items.append({
                'x': x,
                'y': y,
                'type': 'coin',
                'animation_frame': 0,
                'collected': False
            })
        
        # Spawn mushrooms
        mushroom_positions = [
            (450, ground_y - tile_size * 2),
            (850, ground_y - tile_size * 6)
        ]
        
        for x, y in mushroom_positions:
            self.items.append({
                'x': x,
                'y': y,
                'type': 'mushroom',
                'collected': False
            })
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.frame_count += 1
        
        # Update Mario physics
        self.update_mario_physics()
        
        # Update camera
        self.update_camera()
        
        # Update enemies
        self.update_enemies()
        
        # Update items
        self.update_items()
        
        # Check collisions
        self.check_collisions()
    
    def update_mario_physics(self):
        """Update Mario's physics and movement"""
        # Handle horizontal movement
        left_pressed = self.keys_pressed[pygame.K_LEFT]
        right_pressed = self.keys_pressed[pygame.K_RIGHT]
        shift_pressed = self.keys_pressed[pygame.K_LSHIFT] or self.keys_pressed[pygame.K_RSHIFT]
        
        max_speed = config.MARIO_RUN_SPEED if shift_pressed else config.MARIO_WALK_SPEED
        
        if left_pressed:
            self.mario_facing_right = False
            if self.mario_velocity_x > -max_speed:
                friction = config.MARIO_FRICTION if self.mario_on_ground else config.MARIO_AIR_FRICTION
                self.mario_velocity_x -= config.MARIO_ACCELERATION
                self.mario_velocity_x = max(self.mario_velocity_x, -max_speed)
        elif right_pressed:
            self.mario_facing_right = True
            if self.mario_velocity_x < max_speed:
                friction = config.MARIO_FRICTION if self.mario_on_ground else config.MARIO_AIR_FRICTION
                self.mario_velocity_x += config.MARIO_ACCELERATION
                self.mario_velocity_x = min(self.mario_velocity_x, max_speed)
        else:
            # Apply friction
            friction = config.MARIO_FRICTION if self.mario_on_ground else config.MARIO_AIR_FRICTION
            if self.mario_velocity_x > 0:
                self.mario_velocity_x = max(0, self.mario_velocity_x - friction)
            elif self.mario_velocity_x < 0:
                self.mario_velocity_x = min(0, self.mario_velocity_x + friction)
        
        # Handle jumping
        space_pressed = self.keys_pressed[pygame.K_SPACE]
        if space_pressed and self.mario_on_ground:
            self.mario_velocity_y = config.MARIO_JUMP_STRENGTH
            self.mario_on_ground = False
        
        # Apply gravity
        if not self.mario_on_ground:
            self.mario_velocity_y += config.MARIO_GRAVITY
            self.mario_velocity_y = min(self.mario_velocity_y, config.MARIO_MAX_FALL_SPEED)
        
        # Update position
        self.mario_x += self.mario_velocity_x
        self.mario_y += self.mario_velocity_y
        
        # Keep Mario in bounds
        mario_width = config.MARIO_SCALED_TILE_SIZE
        mario_height = config.MARIO_SCALED_TILE_SIZE
        
        if self.mario_x < 0:
            self.mario_x = 0
            self.mario_velocity_x = 0
        if self.mario_x + mario_width > self.level_width:
            self.mario_x = self.level_width - mario_width
            self.mario_velocity_x = 0
        
        # Check if Mario fell off the level
        if self.mario_y > self.level_height:
            self.game_over = True
            high_score.update_high_score(self.score, "mario")
            return
        
        # Update animation
        if self.mario_on_ground:
            if abs(self.mario_velocity_x) > 0.1:
                self.mario_animation_timer += 1
                if self.mario_animation_timer >= 10:
                    self.mario_animation_timer = 0
                    self.mario_animation_frame = (self.mario_animation_frame + 1) % 3
            else:
                self.mario_animation_frame = 0
        else:
            self.mario_animation_frame = 4  # Jump frame
    
    def update_camera(self):
        """Update camera position to follow Mario"""
        # Camera follows Mario with offset
        target_x = self.mario_x - config.MARIO_CAMERA_OFFSET_X
        self.camera_x = max(0, min(target_x, self.level_width - config.SCREEN_WIDTH))
    
    def update_enemies(self):
        """Update enemy positions and AI"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        
        for enemy in self.enemies:
            if not enemy['alive']:
                continue
            
            # Move enemy
            enemy['x'] += enemy['velocity_x']
            
            # Update animation
            enemy['animation_timer'] += 1
            if enemy['animation_timer'] >= 15:
                enemy['animation_timer'] = 0
                enemy['animation_frame'] = (enemy['animation_frame'] + 1) % 2
            
            # Simple AI: turn around at edges or when hitting a wall
            enemy_rect = pygame.Rect(
                enemy['x'],
                enemy['y'],
                tile_size,
                tile_size
            )
            
            # Check if enemy should turn around
            check_x = enemy['x'] + (tile_size if enemy['velocity_x'] > 0 else 0)
            check_y = enemy['y'] + tile_size
            
            # Convert to tile coordinates
            tile_x = int(check_x // tile_size)
            tile_y = int(check_y // tile_size)
            
            # Check bounds
            if tile_x < 0 or tile_x >= len(self.level_data[0]) or tile_y >= len(self.level_data):
                enemy['velocity_x'] = -enemy['velocity_x']
                enemy['facing_right'] = enemy['velocity_x'] > 0
            elif tile_y < len(self.level_data) and tile_x < len(self.level_data[0]):
                # Check if there's no ground ahead
                if self.level_data[tile_y][tile_x] == 0:
                    enemy['velocity_x'] = -enemy['velocity_x']
                    enemy['facing_right'] = enemy['velocity_x'] > 0
    
    def update_items(self):
        """Update item animations"""
        for item in self.items:
            if item['collected']:
                continue
            
            if item['type'] == 'coin':
                item['animation_frame'] += config.COIN_ANIMATION_SPEED
                if item['animation_frame'] >= 3:
                    item['animation_frame'] = 0
    
    def check_collisions(self):
        """Check all collisions"""
        self.check_mario_ground_collision()
        self.check_mario_enemy_collisions()
        self.check_mario_item_collisions()
    
    def check_mario_ground_collision(self):
        """Check collision between Mario and ground/platforms"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        mario_width = tile_size
        mario_height = tile_size
        
        # Mario's collision box
        mario_rect = pygame.Rect(
            self.mario_x,
            self.mario_y,
            mario_width,
            mario_height
        )
        
        # Check collision with level tiles
        self.mario_on_ground = False
        
        # Check tiles around Mario
        start_tile_x = max(0, int(self.mario_x // tile_size) - 1)
        end_tile_x = min(len(self.level_data[0]), int((self.mario_x + mario_width) // tile_size) + 1)
        start_tile_y = max(0, int(self.mario_y // tile_size) - 1)
        end_tile_y = min(len(self.level_data), int((self.mario_y + mario_height) // tile_size) + 1)
        
        for tile_y in range(start_tile_y, end_tile_y):
            for tile_x in range(start_tile_x, end_tile_x):
                if self.level_data[tile_y][tile_x] != 0:  # Not empty
                    tile_rect = pygame.Rect(
                        tile_x * tile_size,
                        tile_y * tile_size,
                        tile_size,
                        tile_size
                    )
                    
                    if mario_rect.colliderect(tile_rect):
                        # Collision detected
                        # Check if Mario is falling and hitting top of tile
                        if self.mario_velocity_y > 0 and mario_rect.bottom > tile_rect.top:
                            # Land on top
                            self.mario_y = tile_rect.top - mario_height
                            self.mario_velocity_y = 0
                            self.mario_on_ground = True
                        elif self.mario_velocity_y < 0 and mario_rect.top < tile_rect.bottom:
                            # Hit bottom of tile
                            self.mario_y = tile_rect.bottom
                            self.mario_velocity_y = 0
                        elif mario_rect.right > tile_rect.left and mario_rect.left < tile_rect.left:
                            # Hit left side
                            self.mario_x = tile_rect.left - mario_width
                            self.mario_velocity_x = 0
                        elif mario_rect.left < tile_rect.right and mario_rect.right > tile_rect.right:
                            # Hit right side
                            self.mario_x = tile_rect.right
                            self.mario_velocity_x = 0
    
    def check_mario_enemy_collisions(self):
        """Check collision between Mario and enemies"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        mario_rect = pygame.Rect(
            self.mario_x,
            self.mario_y,
            tile_size,
            tile_size
        )
        
        for enemy in self.enemies:
            if not enemy['alive']:
                continue
            
            enemy_rect = pygame.Rect(
                enemy['x'],
                enemy['y'],
                tile_size,
                tile_size
            )
            
            if mario_rect.colliderect(enemy_rect):
                # Check if Mario is jumping on enemy (from above)
                if self.mario_velocity_y > 0 and mario_rect.bottom < enemy_rect.top + 10:
                    # Stomp enemy
                    enemy['alive'] = False
                    self.mario_velocity_y = -5  # Small bounce
                    self.score += config.ENEMY_KILL_VALUE
                else:
                    # Mario takes damage / dies
                    self.game_over = True
                    high_score.update_high_score(self.score, "mario")
                    return
    
    def check_mario_item_collisions(self):
        """Check collision between Mario and items"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        mario_rect = pygame.Rect(
            self.mario_x,
            self.mario_y,
            tile_size,
            tile_size
        )
        
        for item in self.items:
            if item['collected']:
                continue
            
            item_rect = pygame.Rect(
                item['x'],
                item['y'],
                tile_size,
                tile_size
            )
            
            if mario_rect.colliderect(item_rect):
                item['collected'] = True
                
                if item['type'] == 'coin':
                    self.score += config.COIN_VALUE
                elif item['type'] == 'mushroom':
                    self.score += config.MUSHROOM_VALUE
    
    def draw(self):
        """Draw the game"""
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Draw background
        self.draw_background()
        
        # Draw level
        self.draw_level()
        
        # Draw items
        self.draw_items()
        
        # Draw enemies
        self.draw_enemies()
        
        # Draw Mario
        self.draw_mario()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_background(self):
        """Draw the background"""
        self.screen.fill(config.MARIO_SKY_BLUE)
    
    def draw_level(self):
        """Draw the level tiles"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        
        # Only draw visible tiles
        start_tile_x = max(0, int(self.camera_x // tile_size) - 1)
        end_tile_x = min(len(self.level_data[0]), int((self.camera_x + config.SCREEN_WIDTH) // tile_size) + 1)
        
        for tile_y in range(len(self.level_data)):
            for tile_x in range(start_tile_x, end_tile_x):
                tile_type = self.level_data[tile_y][tile_x]
                
                if tile_type != 0:  # Not empty
                    screen_x = tile_x * tile_size - self.camera_x
                    screen_y = tile_y * tile_size
                    
                    # Only draw if on screen
                    if -tile_size <= screen_x <= config.SCREEN_WIDTH:
                        sprite_name = None
                        if tile_type == 1:  # Ground
                            sprite_name = 'ground_middle'
                        elif tile_type == 2:  # Brick
                            sprite_name = 'brick'
                        elif tile_type == 3:  # Question block
                            sprite_name = 'question_block'
                        
                        sprite = self.sprites.get_sprite(sprite_name, 'ground_middle')
                        if sprite:
                            self.screen.blit(sprite, (screen_x, screen_y))
                        else:
                            # Fallback rendering
                            color = config.MARIO_GROUND_BROWN if tile_type == 1 else config.MARIO_BRICK_BROWN
                            pygame.draw.rect(self.screen, color, (screen_x, screen_y, tile_size, tile_size))
    
    def draw_mario(self):
        """Draw Mario character"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        screen_x = self.mario_x - self.camera_x
        screen_y = self.mario_y
        
        # Determine which sprite to use
        direction = 'r' if self.mario_facing_right else 'l'
        
        if not self.mario_on_ground:
            sprite_name = f'mario_jump_{direction}'
        elif abs(self.mario_velocity_x) > 0.1:
            walk_frame = self.mario_animation_frame + 1
            sprite_name = f'mario_walk{walk_frame}_{direction}'
        else:
            sprite_name = f'mario_idle_{direction}'
        
        sprite = self.sprites.get_sprite(sprite_name, 'mario_idle_r')
        if sprite:
            self.screen.blit(sprite, (screen_x, screen_y))
        else:
            # Fallback rendering
            color = config.MARIO_MARIO_RED
            pygame.draw.rect(self.screen, color, (screen_x, screen_y, tile_size, tile_size))
            # Draw simple Mario face
            eye_size = 3
            eye_y = screen_y + 5
            if self.mario_facing_right:
                pygame.draw.circle(self.screen, config.BLACK, (screen_x + 5, eye_y), eye_size)
                pygame.draw.circle(self.screen, config.BLACK, (screen_x + 11, eye_y), eye_size)
            else:
                pygame.draw.circle(self.screen, config.BLACK, (screen_x + 5, eye_y), eye_size)
                pygame.draw.circle(self.screen, config.BLACK, (screen_x + 11, eye_y), eye_size)
    
    def draw_enemies(self):
        """Draw enemies"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        
        for enemy in self.enemies:
            if not enemy['alive']:
                continue
            
            screen_x = enemy['x'] - self.camera_x
            screen_y = enemy['y']
            
            # Only draw if on screen
            if -tile_size <= screen_x <= config.SCREEN_WIDTH:
                direction = 'r' if enemy['facing_right'] else 'l'
                frame = enemy['animation_frame'] + 1
                sprite_name = f'koopa_walk{frame}_{direction}'
                
                sprite = self.sprites.get_sprite(sprite_name, 'koopa_walk1_r')
                if sprite:
                    self.screen.blit(sprite, (screen_x, screen_y))
                else:
                    # Fallback rendering
                    color = (0, 150, 0)  # Green for Koopa
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, tile_size, tile_size))
    
    def draw_items(self):
        """Draw items (coins, power-ups)"""
        tile_size = config.MARIO_SCALED_TILE_SIZE
        
        for item in self.items:
            if item['collected']:
                continue
            
            screen_x = item['x'] - self.camera_x
            screen_y = item['y']
            
            # Only draw if on screen
            if -tile_size <= screen_x <= config.SCREEN_WIDTH:
                if item['type'] == 'coin':
                    coin_frame = int(item['animation_frame']) % 3 + 1
                    sprite_name = f'coin{coin_frame}'
                    sprite = self.sprites.get_sprite(sprite_name, 'coin1')
                    if sprite:
                        self.screen.blit(sprite, (screen_x, screen_y))
                    else:
                        # Fallback rendering
                        pygame.draw.circle(self.screen, config.RETRO_YELLOW, 
                                         (screen_x + tile_size // 2, screen_y + tile_size // 2), 
                                         tile_size // 3)
                
                elif item['type'] == 'mushroom':
                    sprite = self.sprites.get_sprite('mushroom')
                    if sprite:
                        self.screen.blit(sprite, (screen_x, screen_y))
                    else:
                        # Fallback rendering
                        pygame.draw.circle(self.screen, (220, 20, 20), 
                                         (screen_x + tile_size // 2, screen_y + tile_size // 2), 
                                         tile_size // 2)
    
    def draw_ui(self):
        """Draw UI elements (score, etc.)"""
        # Draw score
        score_text = self.font_medium.render(f"Score: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER", True, config.WHITE)
            text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over

