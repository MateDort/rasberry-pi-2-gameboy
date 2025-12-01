"""
Mario-style platformer game implementation
"""
import pygame
import random
import config
import high_score

class MarioGame:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()
        self.font_medium = None
        self.font_small = None
        self.frame_count = 0
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Mario properties
        self.mario_x = 100
        self.mario_y = config.SCREEN_HEIGHT - 100
        self.mario_vx = 0
        self.mario_vy = 0
        self.mario_state = "small"  # small, large, fire
        self.mario_facing = "right"  # left or right
        self.mario_on_ground = False
        self.mario_invincible = False
        self.mario_invincible_timer = 0
        
        # Game state
        self.score = 0
        self.lives = config.MARIO_START_LIVES
        self.coins = []
        self.coins_collected = 0
        self.game_over = False
        self.frame_count = 0
        
        # Entities
        self.enemies = []
        self.power_ups = []
        self.blocks = []
        self.coins = []
        self.fireballs = []
        
        # Create level layout
        self.create_level()
        
        # Spawn initial enemies
        self.spawn_enemies()
    
    def create_level(self):
        """Create the level layout with platforms and blocks"""
        # Ground platform (full width at bottom)
        ground_y = config.SCREEN_HEIGHT - 40
        for x in range(0, config.SCREEN_WIDTH, config.BLOCK_SIZE):
            self.blocks.append({
                'type': 'ground',
                'x': x,
                'y': ground_y,
                'width': config.BLOCK_SIZE,
                'height': config.BLOCK_SIZE,
                'breakable': False
            })
        
        # Platform 1 (left side, medium height)
        platform1_y = ground_y - 120
        for x in range(200, 400, config.BLOCK_SIZE):
            self.blocks.append({
                'type': 'platform',
                'x': x,
                'y': platform1_y,
                'width': config.BLOCK_SIZE,
                'height': config.BLOCK_SIZE,
                'breakable': False
            })
            # Add question block above platform
            if x == 250:
                self.blocks.append({
                    'type': 'question',
                    'x': x,
                    'y': platform1_y - config.BLOCK_SIZE,
                    'width': config.BLOCK_SIZE,
                    'height': config.BLOCK_SIZE,
                    'hit': False,
                    'item': random.choice(['coin', 'mushroom', 'fire_flower'])
                })
        
        # Platform 2 (right side, high)
        platform2_y = ground_y - 200
        for x in range(500, 700, config.BLOCK_SIZE):
            self.blocks.append({
                'type': 'platform',
                'x': x,
                'y': platform2_y,
                'width': config.BLOCK_SIZE,
                'height': config.BLOCK_SIZE,
                'breakable': False
            })
            # Add breakable blocks
            if x == 550:
                self.blocks.append({
                    'type': 'breakable',
                    'x': x,
                    'y': platform2_y - config.BLOCK_SIZE,
                    'width': config.BLOCK_SIZE,
                    'height': config.BLOCK_SIZE,
                    'broken': False
                })
        
        # Platform 3 (center, low)
        platform3_y = ground_y - 80
        for x in range(400, 500, config.BLOCK_SIZE):
            self.blocks.append({
                'type': 'platform',
                'x': x,
                'y': platform3_y,
                'width': config.BLOCK_SIZE,
                'height': config.BLOCK_SIZE,
                'breakable': False
            })
            # Add question block
            if x == 450:
                self.blocks.append({
                    'type': 'question',
                    'x': x,
                    'y': platform3_y - config.BLOCK_SIZE,
                    'width': config.BLOCK_SIZE,
                    'height': config.BLOCK_SIZE,
                    'hit': False,
                    'item': random.choice(['coin', 'mushroom', 'fire_flower'])
                })
        
        # Add some floating coins
        self.coins.append({
            'x': 300,
            'y': platform1_y - 50,
            'width': config.COIN_SIZE,
            'height': config.COIN_SIZE,
            'collected': False,
            'animation_frame': 0
        })
        self.coins.append({
            'x': 600,
            'y': platform2_y - 50,
            'width': config.COIN_SIZE,
            'height': config.COIN_SIZE,
            'collected': False,
            'animation_frame': 0
        })
    
    def spawn_enemies(self):
        """Spawn initial enemies"""
        ground_y = config.SCREEN_HEIGHT - 40
        
        # Spawn Goombas
        self.enemies.append({
            'type': 'goomba',
            'x': 300,
            'y': ground_y - 32,
            'width': 24,
            'height': 32,
            'vx': -config.GOOMBA_SPEED,
            'alive': True
        })
        self.enemies.append({
            'type': 'goomba',
            'x': 600,
            'y': ground_y - 32,
            'width': 24,
            'height': 32,
            'vx': -config.GOOMBA_SPEED,
            'alive': True
        })
        
        # Spawn Koopa Troopas
        self.enemies.append({
            'type': 'koopa',
            'x': 450,
            'y': ground_y - 40,
            'width': 24,
            'height': 40,
            'vx': -config.KOOPA_SPEED,
            'alive': True,
            'shell': False  # True when in shell form
        })
    
    def get_mario_rect(self):
        """Get Mario's collision rectangle"""
        if self.mario_state == "small":
            return pygame.Rect(
                self.mario_x - config.MARIO_SMALL_WIDTH // 2,
                self.mario_y - config.MARIO_SMALL_HEIGHT,
                config.MARIO_SMALL_WIDTH,
                config.MARIO_SMALL_HEIGHT
            )
        else:
            return pygame.Rect(
                self.mario_x - config.MARIO_LARGE_WIDTH // 2,
                self.mario_y - config.MARIO_LARGE_HEIGHT,
                config.MARIO_LARGE_WIDTH,
                config.MARIO_LARGE_HEIGHT
            )
    
    def check_platform_collision(self, rect):
        """Check if rectangle collides with any platform"""
        for block in self.blocks:
            if block.get('breakable', False) and block.get('broken', False):
                continue
            block_rect = pygame.Rect(block['x'], block['y'], block['width'], block['height'])
            if rect.colliderect(block_rect):
                return block_rect
        return None
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Jump
                if self.mario_on_ground:
                    self.mario_vy = -config.MARIO_JUMP_STRENGTH
                    self.mario_on_ground = False
            elif event.key == pygame.K_DOWN:
                # Crouch (only when large)
                pass  # Can add crouch animation later
            elif event.key == pygame.K_x or event.key == pygame.K_z:
                # Shoot fireball (only when fire state)
                if self.mario_state == "fire":
                    self.shoot_fireball()
        elif event.type == pygame.KEYUP:
            pass
    
    def shoot_fireball(self):
        """Shoot a fireball"""
        direction = 1 if self.mario_facing == "right" else -1
        mario_rect = self.get_mario_rect()
        self.fireballs.append({
            'x': self.mario_x + (direction * config.MARIO_LARGE_WIDTH // 2),
            'y': self.mario_y - config.MARIO_LARGE_HEIGHT // 2,
            'width': 12,
            'height': 12,
            'vx': direction * config.FIREBALL_SPEED,
            'vy': 0
        })
    
    def update_mario(self):
        """Update Mario's position and physics"""
        # Handle horizontal movement
        keys = pygame.key.get_pressed()
        self.mario_vx = 0
        if keys[pygame.K_LEFT]:
            self.mario_vx = -config.MARIO_RUN_SPEED
            self.mario_facing = "left"
        if keys[pygame.K_RIGHT]:
            self.mario_vx = config.MARIO_RUN_SPEED
            self.mario_facing = "right"
        
        # Apply gravity
        if not self.mario_on_ground:
            self.mario_vy += config.MARIO_GRAVITY
            if self.mario_vy > config.MARIO_MAX_FALL_SPEED:
                self.mario_vy = config.MARIO_MAX_FALL_SPEED
        
        # Update position
        new_x = self.mario_x + self.mario_vx
        new_y = self.mario_y + self.mario_vy
        
        # Check horizontal collision
        mario_rect = self.get_mario_rect()
        mario_rect.x = new_x - mario_rect.width // 2
        mario_rect.y = self.mario_y - mario_rect.height
        
        collision = self.check_platform_collision(mario_rect)
        if collision:
            if self.mario_vx > 0:  # Moving right
                new_x = collision.left - mario_rect.width // 2
            elif self.mario_vx < 0:  # Moving left
                new_x = collision.right + mario_rect.width // 2
            self.mario_vx = 0
        
        # Check vertical collision
        mario_rect = self.get_mario_rect()
        mario_rect.x = new_x - mario_rect.width // 2
        mario_rect.y = new_y - mario_rect.height
        
        collision = self.check_platform_collision(mario_rect)
        self.mario_on_ground = False
        if collision:
            if self.mario_vy > 0:  # Falling
                new_y = collision.top + mario_rect.height
                self.mario_vy = 0
                self.mario_on_ground = True
            elif self.mario_vy < 0:  # Jumping up
                new_y = collision.bottom + mario_rect.height
                self.mario_vy = 0
        
        # Update position
        self.mario_x = new_x
        self.mario_y = new_y
        
        # Check if Mario fell off screen
        if self.mario_y > config.SCREEN_HEIGHT + 100:
            self.mario_die()
        
        # Update invincibility
        if self.mario_invincible:
            self.mario_invincible_timer -= 1
            if self.mario_invincible_timer <= 0:
                self.mario_invincible = False
    
    def mario_die(self):
        """Handle Mario's death"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            high_score.update_high_score(self.score, "mario")
        else:
            # Respawn Mario
            self.mario_x = 100
            self.mario_y = config.SCREEN_HEIGHT - 100
            self.mario_vx = 0
            self.mario_vy = 0
            if self.mario_state != "small":
                self.mario_state = "small"
            self.mario_invincible = True
            self.mario_invincible_timer = config.INVINCIBILITY_TIME
    
    def update_enemies(self):
        """Update enemy positions and AI"""
        for enemy in self.enemies[:]:
            if not enemy['alive']:
                continue
            
            # Update position
            enemy['x'] += enemy['vx']
            
            # Check if enemy hit a wall or platform edge
            enemy_rect = pygame.Rect(
                enemy['x'] - enemy['width'] // 2,
                enemy['y'] - enemy['height'],
                enemy['width'],
                enemy['height']
            )
            
            # Check collision with platforms
            collision = self.check_platform_collision(enemy_rect)
            if collision:
                # Reverse direction
                enemy['vx'] = -enemy['vx']
                enemy['x'] += enemy['vx'] * 2  # Move away from wall
            
            # Check if enemy fell off screen
            if enemy['y'] > config.SCREEN_HEIGHT + 50:
                self.enemies.remove(enemy)
                continue
            
            # Check collision with Mario
            mario_rect = self.get_mario_rect()
            if enemy_rect.colliderect(mario_rect) and not self.mario_invincible:
                # Check if Mario jumped on top
                if (self.mario_vy > 0 and 
                    mario_rect.bottom < enemy_rect.top + 10):
                    # Mario jumped on enemy
                    if enemy['type'] == 'goomba':
                        self.score += 100
                        self.enemies.remove(enemy)
                    elif enemy['type'] == 'koopa':
                        if not enemy.get('shell', False):
                            # Turn into shell
                            enemy['shell'] = True
                            enemy['height'] = 20
                            enemy['vx'] = 0
                            self.score += 200
                        else:
                            # Kick shell
                            direction = 1 if self.mario_x < enemy['x'] else -1
                            enemy['vx'] = direction * config.KOOPA_SHELL_SPEED
                            self.score += 200
                    self.mario_vy = -5  # Small bounce
                else:
                    # Mario hit enemy from side
                    self.mario_die()
    
    def update_power_ups(self):
        """Update power-up positions"""
        for power_up in self.power_ups[:]:
            # Apply gravity
            power_up['vy'] += config.MARIO_GRAVITY * 0.5
            if power_up['vy'] > 5:
                power_up['vy'] = 5
            
            # Update position
            power_up['x'] += power_up['vx']
            power_up['y'] += power_up['vy']
            
            # Check platform collision
            power_up_rect = pygame.Rect(
                power_up['x'] - power_up['width'] // 2,
                power_up['y'] - power_up['height'],
                power_up['width'],
                power_up['height']
            )
            collision = self.check_platform_collision(power_up_rect)
            if collision:
                if power_up['vy'] > 0:  # Falling
                    power_up['y'] = collision.top + power_up['height']
                    power_up['vy'] = 0
                    power_up['vx'] = 0  # Stop horizontal movement on ground
            
            # Check if off screen
            if power_up['y'] > config.SCREEN_HEIGHT + 50:
                self.power_ups.remove(power_up)
                continue
            
            # Check collision with Mario
            mario_rect = self.get_mario_rect()
            if power_up_rect.colliderect(mario_rect):
                if power_up['type'] == 'mushroom':
                    if self.mario_state == "small":
                        self.mario_state = "large"
                    self.score += 1000
                elif power_up['type'] == 'fire_flower':
                    self.mario_state = "fire"
                    self.score += 1000
                self.power_ups.remove(power_up)
    
    def update_blocks(self):
        """Update block states (check if Mario hits blocks from below)"""
        mario_rect = self.get_mario_rect()
        
        for block in self.blocks:
            if block['type'] == 'question' and not block.get('hit', False):
                block_rect = pygame.Rect(block['x'], block['y'], block['width'], block['height'])
                # Check if Mario hits from below
                if (mario_rect.colliderect(block_rect) and 
                    mario_rect.top < block_rect.bottom and
                    mario_rect.top > block_rect.bottom - 10 and
                    self.mario_vy > 0):
                    block['hit'] = True
                    # Spawn item
                    if block['item'] == 'coin':
                        self.coins.append({
                            'x': block['x'] + block['width'] // 2,
                            'y': block['y'] - 20,
                            'width': config.COIN_SIZE,
                            'height': config.COIN_SIZE,
                            'collected': False,
                            'animation_frame': 0
                        })
                        self.score += 200
                    elif block['item'] == 'mushroom':
                        self.power_ups.append({
                            'type': 'mushroom',
                            'x': block['x'] + block['width'] // 2,
                            'y': block['y'] - 20,
                            'width': 24,
                            'height': 24,
                            'vx': 1,
                            'vy': -2
                        })
                    elif block['item'] == 'fire_flower':
                        self.power_ups.append({
                            'type': 'fire_flower',
                            'x': block['x'] + block['width'] // 2,
                            'y': block['y'] - 20,
                            'width': 24,
                            'height': 24,
                            'vx': 0,
                            'vy': 0
                        })
            
            elif block['type'] == 'breakable' and not block.get('broken', False):
                block_rect = pygame.Rect(block['x'], block['y'], block['width'], block['height'])
                # Check if Mario hits from below (and is large)
                if (mario_rect.colliderect(block_rect) and 
                    mario_rect.top < block_rect.bottom and
                    mario_rect.top > block_rect.bottom - 10 and
                    self.mario_vy > 0 and
                    self.mario_state != "small"):
                    block['broken'] = True
                    # Drop coin
                    self.coins.append({
                        'x': block['x'] + block['width'] // 2,
                        'y': block['y'] - 20,
                        'width': config.COIN_SIZE,
                        'height': config.COIN_SIZE,
                        'collected': False,
                        'animation_frame': 0
                    })
                    self.score += 100
    
    def update_coins(self):
        """Update coin states"""
        mario_rect = self.get_mario_rect()
        
        for coin in self.coins[:]:
            if coin.get('collected', False):
                self.coins.remove(coin)
                continue
            
            coin['animation_frame'] += 1
            
            # Check collision with Mario
            coin_rect = pygame.Rect(
                coin['x'] - coin['width'] // 2,
                coin['y'] - coin['height'],
                coin['width'],
                coin['height']
            )
            if coin_rect.colliderect(mario_rect):
                coin['collected'] = True
                self.coins.remove(coin)
                self.coins_collected += 1
                self.score += 100
                
                # Check for extra life
                if self.coins_collected >= config.COINS_PER_LIFE:
                    self.lives += 1
                    self.coins_collected = 0
    
    def update_fireballs(self):
        """Update fireball positions"""
        for fireball in self.fireballs[:]:
            fireball['x'] += fireball['vx']
            fireball['y'] += fireball['vy']
            
            # Check if off screen
            if (fireball['x'] < 0 or fireball['x'] > config.SCREEN_WIDTH or
                fireball['y'] < 0 or fireball['y'] > config.SCREEN_HEIGHT):
                self.fireballs.remove(fireball)
                continue
            
            # Check collision with platforms
            fireball_rect = pygame.Rect(
                fireball['x'] - fireball['width'] // 2,
                fireball['y'] - fireball['height'] // 2,
                fireball['width'],
                fireball['height']
            )
            if self.check_platform_collision(fireball_rect):
                self.fireballs.remove(fireball)
                continue
            
            # Check collision with enemies
            for enemy in self.enemies[:]:
                if not enemy['alive']:
                    continue
                enemy_rect = pygame.Rect(
                    enemy['x'] - enemy['width'] // 2,
                    enemy['y'] - enemy['height'],
                    enemy['width'],
                    enemy['height']
                )
                if fireball_rect.colliderect(enemy_rect):
                    if enemy['type'] == 'goomba':
                        self.score += 100
                        self.enemies.remove(enemy)
                    elif enemy['type'] == 'koopa':
                        self.score += 200
                        self.enemies.remove(enemy)
                    self.fireballs.remove(fireball)
                    break
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.frame_count += 1
        
        # Update all game entities
        self.update_mario()
        self.update_enemies()
        self.update_power_ups()
        self.update_blocks()
        self.update_coins()
        self.update_fireballs()
    
    def draw_mario(self):
        """Draw Mario character"""
        mario_rect = self.get_mario_rect()
        
        # Flash effect when invincible
        if self.mario_invincible and (self.frame_count // 5) % 2 == 0:
            return  # Skip drawing this frame
        
        if self.mario_state == "small":
            # Draw small Mario
            # Body (red)
            body_rect = pygame.Rect(
                mario_rect.x + 4,
                mario_rect.y + 8,
                16,
                16
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, body_rect)
            
            # Head (red)
            head_rect = pygame.Rect(
                mario_rect.x + 4,
                mario_rect.y,
                16,
                12
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, head_rect)
            
            # Hat (red with blue)
            hat_rect = pygame.Rect(
                mario_rect.x + 2,
                mario_rect.y - 4,
                20,
                8
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, hat_rect)
            pygame.draw.rect(self.screen, config.MARIO_BLUE, 
                           (hat_rect.x + 4, hat_rect.y, 12, 4))
        else:
            # Draw large Mario
            # Body (red)
            body_rect = pygame.Rect(
                mario_rect.x + 4,
                mario_rect.y + 24,
                16,
                20
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, body_rect)
            
            # Head (red)
            head_rect = pygame.Rect(
                mario_rect.x + 4,
                mario_rect.y + 8,
                16,
                16
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, head_rect)
            
            # Hat
            hat_rect = pygame.Rect(
                mario_rect.x + 2,
                mario_rect.y + 4,
                20,
                8
            )
            pygame.draw.rect(self.screen, config.MARIO_RED, hat_rect)
            pygame.draw.rect(self.screen, config.MARIO_BLUE, 
                           (hat_rect.x + 4, hat_rect.y, 12, 4))
            
            # Fire state indicator (orange glow)
            if self.mario_state == "fire":
                glow_rect = pygame.Rect(
                    mario_rect.x - 2,
                    mario_rect.y - 2,
                    mario_rect.width + 4,
                    mario_rect.height + 4
                )
                pygame.draw.rect(self.screen, config.MARIO_ORANGE, glow_rect, 2)
    
    def draw_enemies(self):
        """Draw enemies"""
        for enemy in self.enemies:
            if not enemy['alive']:
                continue
            
            enemy_rect = pygame.Rect(
                enemy['x'] - enemy['width'] // 2,
                enemy['y'] - enemy['height'],
                enemy['width'],
                enemy['height']
            )
            
            if enemy['type'] == 'goomba':
                # Draw Goomba (brown mushroom-like)
                pygame.draw.ellipse(self.screen, config.GOOMBA_BROWN, enemy_rect)
                # Eyes
                eye1 = pygame.Rect(enemy_rect.x + 4, enemy_rect.y + 6, 4, 4)
                eye2 = pygame.Rect(enemy_rect.x + 16, enemy_rect.y + 6, 4, 4)
                pygame.draw.ellipse(self.screen, config.BLACK, eye1)
                pygame.draw.ellipse(self.screen, config.BLACK, eye2)
            
            elif enemy['type'] == 'koopa':
                if enemy.get('shell', False):
                    # Draw shell
                    shell_rect = pygame.Rect(
                        enemy_rect.x,
                        enemy_rect.y + 8,
                        enemy_rect.width,
                        12
                    )
                    pygame.draw.ellipse(self.screen, config.KOOPA_GREEN, shell_rect)
                    pygame.draw.ellipse(self.screen, config.BLACK, shell_rect, 2)
                else:
                    # Draw Koopa Troopa
                    # Shell
                    shell_rect = pygame.Rect(
                        enemy_rect.x + 2,
                        enemy_rect.y + 12,
                        enemy_rect.width - 4,
                        16
                    )
                    pygame.draw.ellipse(self.screen, config.KOOPA_GREEN, shell_rect)
                    # Body
                    body_rect = pygame.Rect(
                        enemy_rect.x + 4,
                        enemy_rect.y + 4,
                        enemy_rect.width - 8,
                        12
                    )
                    pygame.draw.rect(self.screen, config.MARIO_BROWN, body_rect)
                    # Head
                    head_rect = pygame.Rect(
                        enemy_rect.x + 6,
                        enemy_rect.y,
                        12,
                        8
                    )
                    pygame.draw.rect(self.screen, config.MARIO_BROWN, head_rect)
    
    def draw_blocks(self):
        """Draw blocks"""
        for block in self.blocks:
            if block.get('broken', False):
                continue
            
            block_rect = pygame.Rect(block['x'], block['y'], block['width'], block['height'])
            
            if block['type'] == 'ground' or block['type'] == 'platform':
                # Brown block
                pygame.draw.rect(self.screen, config.MARIO_BROWN, block_rect)
                pygame.draw.rect(self.screen, config.BLACK, block_rect, 2)
                # Add some texture
                for i in range(0, block['width'], 4):
                    pygame.draw.line(self.screen, (100, 50, 0), 
                                   (block['x'] + i, block['y']),
                                   (block['x'] + i, block['y'] + block['height']), 1)
            
            elif block['type'] == 'question':
                if block.get('hit', False):
                    # Draw as regular block after hit
                    pygame.draw.rect(self.screen, config.MARIO_BROWN, block_rect)
                    pygame.draw.rect(self.screen, config.BLACK, block_rect, 2)
                else:
                    # Yellow question block
                    pygame.draw.rect(self.screen, config.MARIO_YELLOW, block_rect)
                    pygame.draw.rect(self.screen, config.BLACK, block_rect, 2)
                    # Question mark
                    q_text = self.font_small.render("?", True, config.BLACK)
                    q_rect = q_text.get_rect(center=block_rect.center)
                    self.screen.blit(q_text, q_rect)
            
            elif block['type'] == 'breakable':
                # Brown breakable block
                pygame.draw.rect(self.screen, config.MARIO_BROWN, block_rect)
                pygame.draw.rect(self.screen, config.BLACK, block_rect, 2)
                # Add dots pattern
                for i in range(2):
                    for j in range(2):
                        dot_x = block['x'] + 8 + i * 8
                        dot_y = block['y'] + 8 + j * 8
                        pygame.draw.circle(self.screen, (100, 50, 0), (dot_x, dot_y), 2)
    
    def draw_power_ups(self):
        """Draw power-ups"""
        for power_up in self.power_ups:
            power_up_rect = pygame.Rect(
                power_up['x'] - power_up['width'] // 2,
                power_up['y'] - power_up['height'],
                power_up['width'],
                power_up['height']
            )
            
            if power_up['type'] == 'mushroom':
                # Draw mushroom
                # Cap (red)
                cap_rect = pygame.Rect(
                    power_up_rect.x,
                    power_up_rect.y,
                    power_up_rect.width,
                    power_up_rect.height // 2
                )
                pygame.draw.ellipse(self.screen, config.MUSHROOM_RED, cap_rect)
                # Spots
                pygame.draw.circle(self.screen, config.WHITE, 
                                 (power_up_rect.x + 6, power_up_rect.y + 4), 2)
                pygame.draw.circle(self.screen, config.WHITE, 
                                 (power_up_rect.x + 18, power_up_rect.y + 4), 2)
                # Stem (white)
                stem_rect = pygame.Rect(
                    power_up_rect.x + 8,
                    power_up_rect.y + power_up_rect.height // 2,
                    8,
                    power_up_rect.height // 2
                )
                pygame.draw.rect(self.screen, config.MUSHROOM_WHITE, stem_rect)
            
            elif power_up['type'] == 'fire_flower':
                # Draw fire flower
                # Center (yellow)
                center_rect = pygame.Rect(
                    power_up_rect.x + 4,
                    power_up_rect.y + 4,
                    16,
                    16
                )
                pygame.draw.ellipse(self.screen, config.MARIO_YELLOW, center_rect)
                # Petals (red/orange)
                for i in range(4):
                    angle = i * 90
                    petal_x = power_up_rect.centerx + 6 * (1 if i % 2 == 0 else -1)
                    petal_y = power_up_rect.centery + 6 * (1 if (i // 2) % 2 == 0 else -1)
                    pygame.draw.circle(self.screen, config.MARIO_ORANGE, (petal_x, petal_y), 4)
    
    def draw_coins(self):
        """Draw coins"""
        for coin in self.coins:
            if coin.get('collected', False):
                continue
            
            # Animate coin (spin effect)
            coin_rect = pygame.Rect(
                coin['x'] - coin['width'] // 2,
                coin['y'] - coin['height'],
                coin['width'],
                coin['height']
            )
            
            # Draw as ellipse that changes based on animation
            anim = coin['animation_frame'] % 20
            if anim < 10:
                # Horizontal ellipse
                pygame.draw.ellipse(self.screen, config.COIN_YELLOW, coin_rect)
            else:
                # Vertical ellipse
                pygame.draw.ellipse(self.screen, config.COIN_YELLOW, 
                                  (coin_rect.x, coin_rect.y, coin_rect.width, coin_rect.height))
            pygame.draw.ellipse(self.screen, config.BLACK, coin_rect, 1)
    
    def draw_fireballs(self):
        """Draw fireballs"""
        for fireball in self.fireballs:
            fireball_rect = pygame.Rect(
                fireball['x'] - fireball['width'] // 2,
                fireball['y'] - fireball['height'] // 2,
                fireball['width'],
                fireball['height']
            )
            # Draw as orange circle
            pygame.draw.circle(self.screen, config.MARIO_ORANGE, 
                             (fireball['x'], fireball['y']), fireball['width'] // 2)
            pygame.draw.circle(self.screen, config.RETRO_YELLOW, 
                             (fireball['x'], fireball['y']), fireball['width'] // 2 - 2)
    
    def draw(self):
        """Draw the game"""
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Draw background (sky)
        self.screen.fill(config.MARIO_SKY)
        
        # Draw clouds (simple white circles)
        cloud_positions = [(150, 100), (400, 80), (650, 120)]
        for x, y in cloud_positions:
            pygame.draw.circle(self.screen, config.WHITE, (x, y), 20)
            pygame.draw.circle(self.screen, config.WHITE, (x + 15, y), 18)
            pygame.draw.circle(self.screen, config.WHITE, (x + 30, y), 20)
        
        # Draw blocks/platforms
        self.draw_blocks()
        
        # Draw coins
        self.draw_coins()
        
        # Draw power-ups
        self.draw_power_ups()
        
        # Draw enemies
        self.draw_enemies()
        
        # Draw fireballs
        self.draw_fireballs()
        
        # Draw Mario
        self.draw_mario()
        
        # Draw UI
        # Score
        score_text = self.font_small.render(f"SCORE: {self.score}", True, config.BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font_small.render(f"LIVES: {self.lives}", True, config.BLACK)
        self.screen.blit(lives_text, (10, 35))
        
        # Coins
        coins_text = self.font_small.render(f"COINS: {self.coins_collected}", True, config.BLACK)
        self.screen.blit(coins_text, (10, 60))
        
        # Instructions
        if self.mario_state == "fire":
            fire_text = self.font_small.render("Press X/Z to shoot fireball", True, config.BLACK)
            self.screen.blit(fire_text, (config.SCREEN_WIDTH - 250, 10))
        
        pygame.display.flip()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over

