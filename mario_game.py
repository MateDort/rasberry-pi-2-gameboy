"""
Super Mario platformer game implementation
Wrapper for the super-mario-python-master codebase
"""
import pygame
import sys
import os
import config
import high_score

# Add the super-mario-python-master directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'super-mario-python-master'))

from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Sound import Sound
from entities.Mario import Mario

class MarioGame:
    def __init__(self, screen):
        self.screen = screen
        self.original_screen = screen
        
        # Store original working directory
        self.original_cwd = os.getcwd()
        
        # Get absolute path to super-mario-python-master directory
        current_file = os.path.abspath(__file__)
        project_dir = os.path.dirname(os.path.dirname(current_file))
        mario_dir = os.path.join(project_dir, 'super-mario-python-master')
        self.mario_dir = mario_dir
        
        # Change to super-mario-python-master directory for asset loading
        if os.path.exists(mario_dir):
            os.chdir(mario_dir)
        
        # Initialize game components
        try:
            self.dashboard = Dashboard("./img/font.png", 8, screen)
            self.sound = Sound()
            self.level = Level(screen, self.sound, self.dashboard)
            
            # Load first level
            self.level.loadLevel("Level1-1")
            
            # Create Mario
            self.mario = Mario(0, 0, self.level, screen, self.dashboard, self.sound)
            
            # Game state
            self.game_over = False
            self.score = 0
            self.keys_pressed = {}
            
            # Override Mario's input to work with our event system
            self._setup_custom_input()
            
        except Exception as e:
            print(f"Error initializing Mario game: {e}")
            import traceback
            traceback.print_exc()
            self.game_over = True
        finally:
            # Restore original working directory
            os.chdir(self.original_cwd)
    
    def _setup_custom_input(self):
        """Setup custom input handling that works with our event system"""
        # Store reference to original input
        self.original_input = self.mario.input
        
        # Create a custom input handler
        class CustomInput:
            def __init__(self, mario_game):
                self.mario_game = mario_game
                self.entity = mario_game.mario
            
            def checkForInput(self):
                """Check for input using stored key states"""
                pressed_keys = pygame.key.get_pressed()
                
                # Handle movement
                if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_h]:
                    if not pressed_keys[pygame.K_RIGHT]:
                        self.entity.traits["goTrait"].direction = -1
                elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_l]:
                    if not pressed_keys[pygame.K_LEFT]:
                        self.entity.traits["goTrait"].direction = 1
                else:
                    self.entity.traits['goTrait'].direction = 0
                
                # Handle jumping
                is_jumping = pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_k]
                self.entity.traits['jumpTrait'].jump(is_jumping)
                
                # Handle boost
                self.entity.traits['goTrait'].boost = pressed_keys[pygame.K_LSHIFT]
        
        # Replace input with custom one
        self.mario.input = CustomInput(self)
    
    def handle_event(self, event):
        """Handle input events"""
        # Store key states for the custom input handler
        if event.type == pygame.KEYDOWN:
            self.keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keys_pressed[event.key] = False
    
    def update(self):
        """Update game state"""
        if self.game_over or self.mario.restart:
            return
        
        # Change to mario directory for asset access
        if os.path.exists(self.mario_dir):
            os.chdir(self.mario_dir)
        
        try:
            # Check for input
            self.mario.input.checkForInput()
            
            # Update Mario
            if self.mario.pause:
                if hasattr(self.mario, 'pauseObj'):
                    self.mario.pauseObj.update()
            else:
                self.mario.update()
            
            # Update score from dashboard
            self.score = self.dashboard.points
            
            # Check if game is over
            if self.mario.restart:
                self.game_over = True
                high_score.update_high_score(self.score, "mario")
        
        except Exception as e:
            print(f"Error updating Mario game: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Restore original working directory
            os.chdir(self.original_cwd)
    
    def draw(self):
        """Draw the game"""
        if self.game_over:
            return
        
        # Change to mario directory for asset access
        if os.path.exists(self.mario_dir):
            os.chdir(self.mario_dir)
        
        try:
            if self.mario.pause:
                if hasattr(self.mario, 'pauseObj'):
                    self.mario.pauseObj.update()
            else:
                # Draw level
                self.level.drawLevel(self.mario.camera)
                
                # Update dashboard (draws UI)
                self.dashboard.update()
                
                # Mario is drawn as part of level.drawLevel()
            
        except Exception as e:
            print(f"Error drawing Mario game: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Restore original working directory
            os.chdir(self.original_cwd)
        
        pygame.display.flip()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over or (hasattr(self.mario, 'restart') and self.mario.restart)
