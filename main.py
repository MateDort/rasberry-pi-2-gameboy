"""
Main entry point for the Game Boy Games
Handles game state management and screen transitions
"""
import pygame
import sys
import config
from lobby import Lobby
from loading_screen import LoadingScreen
from snake_game import SnakeGame
from flappy_bird import FlappyBird
from sudoku_game import SudokuGame
from mario_game import MarioGame
from game_over import GameOver

# Game states
STATE_LOBBY = "lobby"
STATE_LOADING = "loading"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"

def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Game Boy Games")
    clock = pygame.time.Clock()
    
    # Initialize game states
    current_state = STATE_LOBBY
    lobby = Lobby(screen)
    loading_screen = LoadingScreen(screen)
    current_game = None
    current_game_type = None
    game_over = None
    
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Route events to current state
            if current_state == STATE_LOBBY:
                result = lobby.handle_event(event)
                if result and result.startswith("start_game:"):
                    current_game_type = result.split(":")[1]  # Get game type
                    current_state = STATE_LOADING
                    loading_screen.start()
            
            elif current_state == STATE_LOADING:
                # Loading screen doesn't handle events, just wait
                pass
            
            elif current_state == STATE_GAME:
                if current_game:
                    current_game.handle_event(event)
            
            elif current_state == STATE_GAME_OVER:
                if game_over:
                    result = game_over.handle_event(event)
                    if result == "restart_game":
                        current_state = STATE_LOADING
                        loading_screen.start()
                        current_game = None  # Will be recreated after loading
                    elif result == "return_lobby":
                        current_state = STATE_LOBBY
                        current_game = None
                        current_game_type = None
                        game_over = None
        
        # Update game state
        if current_state == STATE_LOADING:
            loading_screen.draw()
            if loading_screen.is_complete():
                current_state = STATE_GAME
                if current_game_type == "snake":
                    current_game = SnakeGame(screen)
                elif current_game_type == "flappy_bird":
                    current_game = FlappyBird(screen)
                elif current_game_type == "sudoku":
                    current_game = SudokuGame(screen)
                elif current_game_type == "mario":
                    try:
                        current_game = MarioGame(screen)
                    except (ImportError, Exception) as e:
                        print(f"Error initializing Mario game: {e}")
                        import traceback
                        traceback.print_exc()
                        # Set game_over immediately so we can return to lobby
                        current_state = STATE_LOBBY
                        current_game = None
                        current_game_type = None
        
        elif current_state == STATE_GAME:
            if current_game:
                current_game.update()
                current_game.draw()
                if current_game.is_game_over():
                    current_state = STATE_GAME_OVER
                    game_over = GameOver(screen, current_game.score, current_game_type)
        
        elif current_state == STATE_GAME_OVER:
            if game_over:
                game_over.draw()
        
        elif current_state == STATE_LOBBY:
            lobby.draw()
        
        # Cap frame rate
        clock.tick(config.FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

