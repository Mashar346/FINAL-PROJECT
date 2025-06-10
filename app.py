import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 400
CELL_SIZE = BOARD_SIZE // 3

# Colors
BACKGROUND = (25, 30, 45)
GRID_COLOR = (70, 130, 180)
X_COLOR = (220, 20, 60)    # Crimson
O_COLOR = (30, 180, 30)    # Lime green
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (50, 100, 150)
BUTTON_HOVER = (70, 130, 180)
BUTTON_TEXT = (220, 220, 220)
HIGHLIGHT = (255, 215, 0)  # Gold
AI_COLOR = (180, 70, 180)  # Purple
PLAYER_COLOR = (70, 130, 230) # Steel blue

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe with AI")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("arial", 48, bold=True)
status_font = pygame.font.SysFont("arial", 32)
button_font = pygame.font.SysFont("arial", 28)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Player is X, AI is O
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.difficulty = "HARD"  # Default difficulty
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        
    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None
        
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return False
            
        self.board[row][col] = self.current_player
        self.check_winner()
        
        if not self.game_over:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        return True
    
    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        lines = []
        for i in range(3):
            lines.append([(i, 0), (i, 1), (i, 2)]) # Rows
            lines.append([(0, i), (1, i), (2, i)]) # Columns
        lines.append([(0, 0), (1, 1), (2, 2)])     # Diagonal top-left to bottom-right
        lines.append([(0, 2), (1, 1), (2, 0)])     # Diagonal top-right to bottom-left

        for line_coords in lines:
            symbols = [self.board[r][c] for r, c in line_coords]
            if symbols[0] == symbols[1] == symbols[2] and symbols[0] != '':
                self.winner = symbols[0]
                # Determine winning line for drawing
                if line_coords[0][0] == line_coords[1][0]: self.winning_line = ('row', line_coords[0][0])
                elif line_coords[0][1] == line_coords[1][1]: self.winning_line = ('col', line_coords[0][1])
                elif line_coords[0] == (0,0) and line_coords[2] == (2,2): self.winning_line = ('diag', 0)
                else: self.winning_line = ('diag', 1)
                
                self.game_over = True
                self.update_score()
                return
            
        # Check for draw
        if all(cell != '' for row in self.board for cell in row):
            self.game_over = True
            self.winner = 'Draw'
            self.update_score()
            
    def update_score(self):
        if self.winner == 'X':
            self.player_score += 1
        elif self.winner == 'O':
            self.ai_score += 1
        elif self.winner == 'Draw':
            self.draws += 1
    
    def ai_move(self):
        if self.game_over:
            return
            
        if self.difficulty == "EASY":
            self._random_move()
        elif self.difficulty == "MEDIUM":
            if random.random() < 0.5:  # 50% chance to make a smart move
                self._smart_move()
            else:
                self._random_move()
        else:  # HARD
            self._smart_move()
            
        self.check_winner()
        if not self.game_over:
            self.current_player = 'X'
    
    def _random_move(self):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty_cells.append((row, col))
                    
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'
    
    def _smart_move(self):
        # Check if AI can win in the next move or block player's win
        for player in ['O', 'X']:
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = player
                        temp_winner = self._check_temp_winner()
                        if temp_winner == player:
                            self.board[row][col] = 'O' if player == 'O' else '' # Make the move if AI wins, else revert
                            if player == 'O': return # AI makes the winning move
                            if player == 'X': # AI blocks player's winning move
                                self.board[row][col] = 'O'
                                return
                        self.board[row][col] = '' # Revert
        
        # Try to take the center
        if self.board[1][1] == '':
            self.board[1][1] = 'O'
            return
            
        # Try to take a corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners) # Randomize corner choice
        for row, col in corners:
            if self.board[row][col] == '':
                self.board[row][col] = 'O'
                return
                
        # Take any empty cell
        self._random_move()

    def _check_temp_winner(self):
        # Temporary check for winner without updating game state
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text_surface = button_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

def draw_board(game):
    board_rect = pygame.Rect(
        (WIDTH - BOARD_SIZE) // 2,
        (HEIGHT - BOARD_SIZE) // 2,
        BOARD_SIZE,
        BOARD_SIZE
    )
    pygame.draw.rect(screen, (30, 35, 50), board_rect, border_radius=15)
    
    for i in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, (board_rect.left + i * CELL_SIZE, board_rect.top + 10),
                         (board_rect.left + i * CELL_SIZE, board_rect.bottom - 10), 8)
        pygame.draw.line(screen, GRID_COLOR, (board_rect.left + 10, board_rect.top + i * CELL_SIZE),
                         (board_rect.right - 10, board_rect.top + i * CELL_SIZE), 8)
    
    for row in range(3):
        for col in range(3):
            cell_rect = pygame.Rect(
                board_rect.left + col * CELL_SIZE + 10,
                board_rect.top + row * CELL_SIZE + 10,
                CELL_SIZE - 20,
                CELL_SIZE - 20
            )
            
            if game.board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (cell_rect.left, cell_rect.top),
                                 (cell_rect.right, cell_rect.bottom), 12)
                pygame.draw.line(screen, X_COLOR, (cell_rect.right, cell_rect.top),
                                 (cell_rect.left, cell_rect.bottom), 12)
                
            elif game.board[row][col] == 'O':
                center = cell_rect.center
                pygame.draw.circle(screen, O_COLOR, center, CELL_SIZE // 3, 12)
    
    # Draw winning line
    if game.winning_line:
        line_type, index = game.winning_line
        if line_type == 'row':
            start_pos = (board_rect.left + 50, board_rect.top + (index + 0.5) * CELL_SIZE)
            end_pos = (board_rect.right - 50, board_rect.top + (index + 0.5) * CELL_SIZE)
        elif line_type == 'col':
            start_pos = (board_rect.left + (index + 0.5) * CELL_SIZE, board_rect.top + 50)
            end_pos = (board_rect.left + (index + 0.5) * CELL_SIZE, board_rect.bottom - 50)
        elif line_type == 'diag':
            if index == 0:  # Top-left to bottom-right
                start_pos = (board_rect.left + 50, board_rect.top + 50)
                end_pos = (board_rect.right - 50, board_rect.bottom - 50)
            else:  # Top-right to bottom-left
                start_pos = (board_rect.right - 50, board_rect.top + 50)
                end_pos = (board_rect.left + 50, board_rect.bottom - 50)
        
        pygame.draw.line(screen, HIGHLIGHT, start_pos, end_pos, 10)

def draw_ui(game, buttons):
    title_text = title_font.render("TIC-TAC-TOE", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    diff_color = AI_COLOR if game.difficulty == "HARD" else \
                 O_COLOR if game.difficulty == "MEDIUM" else \
                 X_COLOR
    diff_text = status_font.render(f"Difficulty: {game.difficulty}", True, diff_color)
    screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, 80))
    
    if game.game_over:
        if game.winner == 'X':
            status_text = "You Win!"
            color = PLAYER_COLOR
        elif game.winner == 'O':
            status_text = "AI Wins!"
            color = AI_COLOR
        else:
            status_text = "It's a Draw!"
            color = TEXT_COLOR
    else:
        status_text = "Your Turn" if game.current_player == 'X' else "AI's Turn"
        color = PLAYER_COLOR if game.current_player == 'X' else AI_COLOR
    
    status_surface = status_font.render(status_text, True, color)
    screen.blit(status_surface, (WIDTH // 2 - status_surface.get_width() // 2, HEIGHT - 80))
    
    score_text = status_font.render(
        f"Player: {game.player_score}  AI: {game.ai_score}  Draws: {game.draws}", 
        True, 
        TEXT_COLOR
    )
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 40))
    
    for button in buttons:
        button.draw()

def change_difficulty(game_instance, difficulty):
    game_instance.difficulty = difficulty

def main():
    game = TicTacToe()
    
    # Calculate button x-position for better alignment
    # Let's center the buttons within the left 1/3 of the screen for example.
    # Or simply provide a fixed padding from the left.
    # Current left padding is 50. Let's aim to center them in the first 250 pixels.
    button_area_width = 250
    button_x_start = (button_area_width - 180) // 2 # 180 is button width
    
    buttons = [
        Button(button_x_start, 150, 150, 50, "EASY", lambda: change_difficulty(game, "EASY")),
        Button(button_x_start, 220, 150, 50, "MEDIUM", lambda: change_difficulty(game, "MEDIUM")),
        Button(button_x_start, 290, 150, 50, "HARD", lambda: change_difficulty(game, "HARD")),
        Button(button_x_start, 380, 150, 50, "RESET GAME", game.reset),
        Button(button_x_start, 450, 150, 50, "QUIT", sys.exit)
    ]
    
    ai_move_delay = 0
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            for button in buttons:
                button.check_hover(mouse_pos)
                button.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                if game.current_player == 'X':
                    x, y = event.pos
                    board_rect = pygame.Rect(
                        (WIDTH - BOARD_SIZE) // 2,
                        (HEIGHT - BOARD_SIZE) // 2,
                        BOARD_SIZE,
                        BOARD_SIZE
                    )
                    
                    if board_rect.collidepoint(x, y):
                        col = (x - board_rect.left) // CELL_SIZE
                        row = (y - board_rect.top) // CELL_SIZE
                        
                        if game.make_move(row, col):
                            ai_move_delay = 30 # Delay in frames (e.g., 0.5 seconds at 60 FPS)
        
        if ai_move_delay > 0:
            ai_move_delay -= 1
            if ai_move_delay == 0 and game.current_player == 'O' and not game.game_over:
                game.ai_move()
        
        screen.fill(BACKGROUND)
        
        # Draw decorative elements
        for _ in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            color = (random.randint(50, 150), random.randint(50, 150), random.randint(150, 200))
            pygame.draw.circle(screen, color, (x, y), size)
        
        draw_board(game)
        draw_ui(game, buttons)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()