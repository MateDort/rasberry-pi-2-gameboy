"""
Sudoku game implementation
"""
import pygame
import random
import config
import high_score
import time

class SudokuGame:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.clock = pygame.time.Clock()
        self.start_time = None
        self.elapsed_time = 0
        self.paused = False
        
    def initialize_fonts(self):
        """Initialize fonts"""
        self.font_large = pygame.font.Font(None, config.FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.selected_row = 0
        self.selected_col = 0
        self.difficulty = "medium"  # Default difficulty
        self.game_over = False
        self.won = False
        self.score = 0
        self.start_time = None
        self.elapsed_time = 0
        self.paused = False
        self.show_difficulty_menu = True
        self.difficulty_selected = 0  # 0=Easy, 1=Medium, 2=Hard
        
        # Generate puzzle after difficulty is selected
        # Will be called from handle_event when difficulty is chosen
    
    def generate_solved_puzzle(self):
        """Generate a valid solved Sudoku puzzle"""
        # Start with a valid base pattern
        base = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8]
        ]
        
        # Shuffle rows within each 3x3 block
        for block in range(3):
            rows = list(range(block * 3, block * 3 + 3))
            random.shuffle(rows)
            base[block*3:(block+1)*3] = [base[r] for r in rows]
        
        # Shuffle columns within each 3x3 block
        for block in range(3):
            cols = list(range(block * 3, block * 3 + 3))
            random.shuffle(cols)
            for row in base:
                row[block*3:(block+1)*3] = [row[c] for c in cols]
        
        # Random swaps of rows/columns between blocks
        for _ in range(10):
            if random.random() < 0.5:
                # Swap two rows in different blocks
                block1 = random.randint(0, 2)
                block2 = random.randint(0, 2)
                if block1 != block2:
                    row1 = random.randint(0, 2) + block1 * 3
                    row2 = random.randint(0, 2) + block2 * 3
                    base[row1], base[row2] = base[row2], base[row1]
            else:
                # Swap two columns in different blocks
                block1 = random.randint(0, 2)
                block2 = random.randint(0, 2)
                if block1 != block2:
                    col1 = random.randint(0, 2) + block1 * 3
                    col2 = random.randint(0, 2) + block2 * 3
                    for row in base:
                        row[col1], row[col2] = row[col2], row[col1]
        
        return base
    
    def generate_puzzle(self, difficulty):
        """Generate a Sudoku puzzle with given difficulty"""
        # Generate a solved puzzle
        solved = self.generate_solved_puzzle()
        
        # Copy to grid
        self.grid = [row[:] for row in solved]
        self.original_grid = [row[:] for row in solved]
        
        # Determine how many cells to remove based on difficulty
        if difficulty == "easy":
            cells_to_remove = random.randint(40, 45)
        elif difficulty == "medium":
            cells_to_remove = random.randint(30, 35)
        else:  # hard
            cells_to_remove = random.randint(20, 25)
        
        # Remove cells randomly
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, (row, col) in enumerate(cells):
            if i >= cells_to_remove:
                break
            self.grid[row][col] = 0
            self.original_grid[row][col] = 0
    
    def is_valid_move(self, row, col, num):
        """Check if placing num at (row, col) is valid"""
        if num == 0:
            return True  # Clearing is always valid
        
        # Check row
        for c in range(9):
            if c != col and self.grid[row][c] == num:
                return False
        
        # Check column
        for r in range(9):
            if r != row and self.grid[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.grid[r][c] == num:
                    return False
        
        return True
    
    def check_win(self):
        """Check if the puzzle is complete and correct"""
        # Check if all cells are filled
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return False
        
        # Check if all cells are valid
        for row in range(9):
            for col in range(9):
                num = self.grid[row][col]
                if not self.is_valid_move(row, col, num):
                    return False
        
        return True
    
    def handle_event(self, event):
        """Handle input events"""
        if self.show_difficulty_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.difficulty_selected = (self.difficulty_selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.difficulty_selected = (self.difficulty_selected + 1) % 3
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    difficulties = ["easy", "medium", "hard"]
                    self.difficulty = difficulties[self.difficulty_selected]
                    self.generate_puzzle(self.difficulty)
                    self.show_difficulty_menu = False
                    self.start_time = time.time()
            return
        
        if self.game_over or self.won:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_row = max(0, self.selected_row - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_row = min(8, self.selected_row + 1)
            elif event.key == pygame.K_LEFT:
                self.selected_col = max(0, self.selected_col - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_col = min(8, self.selected_col + 1)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                              pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                # Only allow input if cell is not an original clue
                if self.original_grid[self.selected_row][self.selected_col] == 0:
                    num = int(event.unicode)
                    if self.is_valid_move(self.selected_row, self.selected_col, num):
                        self.grid[self.selected_row][self.selected_col] = num
                    else:
                        # Still place it but mark as invalid (will show in red)
                        self.grid[self.selected_row][self.selected_col] = num
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                # Only allow clearing if cell is not an original clue
                if self.original_grid[self.selected_row][self.selected_col] == 0:
                    self.grid[self.selected_row][self.selected_col] = 0
    
    def update(self):
        """Update game state"""
        if self.show_difficulty_menu or self.game_over or self.won:
            return
        
        if not self.paused and self.start_time:
            self.elapsed_time = time.time() - self.start_time
        
        # Check for win condition
        if self.check_win():
            self.won = True
            self.game_over = True
            # Calculate score: lower time = higher score, adjusted by difficulty
            difficulty_multiplier = {"easy": 1, "medium": 2, "hard": 3}
            # Score is based on time (inverse) and difficulty
            # Use a formula: (max_time - elapsed_time) * multiplier
            # For simplicity, use elapsed_time in seconds as base, inverted
            max_time = 3600  # 1 hour max
            time_score = max(0, max_time - int(self.elapsed_time))
            self.score = time_score * difficulty_multiplier[self.difficulty]
            high_score.update_high_score(self.score, "sudoku")
    
    def draw_difficulty_menu(self):
        """Draw the difficulty selection menu"""
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Background
        self.screen.fill(config.DARK_GREEN)
        
        # Decorative pattern
        for i in range(0, config.SCREEN_WIDTH + config.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (20, 60, 35), 
                           (i, 0), (i - config.SCREEN_HEIGHT, config.SCREEN_HEIGHT), 1)
        
        # Borders
        pygame.draw.rect(self.screen, config.BLACK, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 8)
        pygame.draw.rect(self.screen, config.PURPLE, (10, 10, config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 20), 3)
        
        # Title
        title_text = self.font_large.render("SUDOKU", True, config.PURPLE)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 150))
        # Outline
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    outline_rect = title_rect.copy()
                    outline_rect.x += dx
                    outline_rect.y += dy
                    outline_text = self.font_large.render("SUDOKU", True, config.BLACK)
                    self.screen.blit(outline_text, outline_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("SELECT DIFFICULTY", True, config.PURPLE)
        subtitle_rect = subtitle_text.get_rect(center=(config.SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Difficulty options
        difficulties = ["EASY", "MEDIUM", "HARD"]
        start_y = config.SCREEN_HEIGHT // 2 - 50
        for i, diff in enumerate(difficulties):
            y_pos = start_y + i * 100
            
            # Highlight selected
            if i == self.difficulty_selected:
                box_rect = pygame.Rect(
                    config.SCREEN_WIDTH // 2 - 180,
                    y_pos - 15,
                    360,
                    70
                )
                pygame.draw.rect(self.screen, config.PURPLE, box_rect)
                pygame.draw.rect(self.screen, config.BLACK, box_rect, 4)
                pygame.draw.rect(self.screen, (180, 50, 255), 
                               (box_rect.x + 4, box_rect.y + 4, box_rect.width - 8, box_rect.height - 8), 2)
                color = config.BLACK
            else:
                color = config.PURPLE
            
            diff_text = self.font_medium.render(diff, True, color)
            diff_rect = diff_text.get_rect(center=(config.SCREEN_WIDTH // 2, y_pos + 20))
            self.screen.blit(diff_text, diff_rect)
        
        # Instructions
        instruction_text = self.font_small.render("PRESS ENTER TO START", True, config.PURPLE)
        instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 80))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw(self):
        """Draw the game"""
        if self.show_difficulty_menu:
            self.draw_difficulty_menu()
            pygame.display.flip()
            return
        
        if self.font_medium is None:
            self.initialize_fonts()
        
        # Background
        self.screen.fill(config.DARK_GREEN)
        
        # Calculate grid dimensions
        grid_size = 450  # Total grid size
        cell_size = grid_size // 9
        grid_x = (config.SCREEN_WIDTH - grid_size) // 2
        grid_y = 100
        
        # Draw timer
        if self.start_time and not self.paused:
            minutes = int(self.elapsed_time) // 60
            seconds = int(self.elapsed_time) % 60
            timer_text = self.font_small.render(f"TIME: {minutes:02d}:{seconds:02d}", True, config.WHITE)
            timer_rect = timer_text.get_rect()
            timer_rect.topright = (config.SCREEN_WIDTH - 10, 10)
            self.screen.blit(timer_text, timer_rect)
        
        # Draw difficulty
        diff_text = self.font_small.render(f"DIFFICULTY: {self.difficulty.upper()}", True, config.WHITE)
        self.screen.blit(diff_text, (10, 10))
        
        # Draw grid background
        grid_rect = pygame.Rect(grid_x, grid_y, grid_size, grid_size)
        pygame.draw.rect(self.screen, config.WHITE, grid_rect)
        pygame.draw.rect(self.screen, config.BLACK, grid_rect, 3)
        
        # Draw cells
        for row in range(9):
            for col in range(9):
                cell_x = grid_x + col * cell_size
                cell_y = grid_y + row * cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                
                # Highlight selected cell
                if row == self.selected_row and col == self.selected_col:
                    pygame.draw.rect(self.screen, (200, 150, 255), cell_rect)
                
                # Draw cell border
                border_width = 1
                if col % 3 == 0:
                    border_width = 2
                if row % 3 == 0:
                    border_width = 2
                pygame.draw.rect(self.screen, config.BLACK, cell_rect, border_width)
                
                # Draw number
                num = self.grid[row][col]
                if num != 0:
                    # Check if it's an original clue or user input
                    is_original = self.original_grid[row][col] != 0
                    is_valid = self.is_valid_move(row, col, num)
                    
                    if is_original:
                        color = config.BLACK
                        font = self.font_medium
                    else:
                        # User input: green if valid, red if invalid
                        if is_valid:
                            color = (0, 150, 0)  # Dark green
                        else:
                            color = (200, 0, 0)  # Red
                        font = self.font_small
                    
                    num_text = font.render(str(num), True, color)
                    num_rect = num_text.get_rect(center=(cell_x + cell_size // 2, cell_y + cell_size // 2))
                    self.screen.blit(num_text, num_rect)
        
        # Draw win message
        if self.won:
            # Semi-transparent overlay
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(config.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.font_large.render("PUZZLE SOLVED!", True, config.PURPLE)
            win_rect = win_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
            # Outline
            for dx in [-3, 0, 3]:
                for dy in [-3, 0, 3]:
                    if dx != 0 or dy != 0:
                        outline_rect = win_rect.copy()
                        outline_rect.x += dx
                        outline_rect.y += dy
                        outline_text = self.font_large.render("PUZZLE SOLVED!", True, config.BLACK)
                        self.screen.blit(outline_text, outline_rect)
            self.screen.blit(win_text, win_rect)
            
            minutes = int(self.elapsed_time) // 60
            seconds = int(self.elapsed_time) % 60
            time_text = self.font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, config.PURPLE)
            time_rect = time_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(time_text, time_rect)
        
        pygame.display.flip()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.game_over

