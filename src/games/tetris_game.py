import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_X = (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Tetris pieces
TETRIS_PIECES = [
    [['.....',
      '..#..',
      '.###.',
      '.....',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '.#...',
      '.....']],
    [['.....',
      '.....',
      '.###.',
      '.#...',
      '.....'],
     ['.....',
      '.##..',
      '..#..',
      '..#..',
      '.....']],
    [['.....',
      '.....',
      '.###.',
      '...#.',
      '.....'],
     ['.....',
      '..#..',
      '..#..',
      '.##..',
      '.....']],
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    [['.....',
      '.....',
      '.##..',
      '..##.',
      '.....'],
     ['.....',
      '..#..',
      '.##..',
      '.#...',
      '.....']],
    [['.....',
      '.....',
      '..##.',
      '.##..',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '..#..',
      '.....']],
    [['.....',
      '.....',
      '####.',
      '.....',
      '.....'],
     ['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..']]
]

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        
    def new_piece(self):
        piece_type = random.randint(0, len(TETRIS_PIECES) - 1)
        return {
            'type': piece_type,
            'rotation': 0,
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'shape': TETRIS_PIECES[piece_type][0]
        }
    
    def rotate_piece(self, piece):
        rotations = TETRIS_PIECES[piece['type']]
        piece['rotation'] = (piece['rotation'] + 1) % len(rotations)
        piece['shape'] = rotations[piece['rotation']]
    
    def valid_move(self, piece, dx, dy):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True
    
    def place_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    grid_x = piece['x'] + x
                    grid_y = piece['y'] + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = piece['type'] + 1
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        cleared = len(lines_to_clear)
        self.lines_cleared += cleared
        self.score += cleared * 100 * self.level
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def game_over(self):
        return not self.valid_move(self.current_piece, 0, 0)
    
    def update(self, dt):
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.valid_move(self.current_piece, 0, 1):
                self.current_piece['y'] += 1
            else:
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()
            self.fall_time = 0
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(GRID_X + x * BLOCK_SIZE, GRID_Y + y * BLOCK_SIZE, 
                                 BLOCK_SIZE, BLOCK_SIZE)
                if self.grid[y][x]:
                    color = COLORS[(self.grid[y][x] - 1) % len(COLORS)]
                    pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)
        
        # Draw current piece
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(GRID_X + (self.current_piece['x'] + x) * BLOCK_SIZE,
                                     GRID_Y + (self.current_piece['y'] + y) * BLOCK_SIZE,
                                     BLOCK_SIZE, BLOCK_SIZE)
                    color = COLORS[self.current_piece['type'] % len(COLORS)]
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        lines_text = font.render(f'Lines: {self.lines_cleared}', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(lines_text, (10, 90))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    game = TetrisGame()
    
    while True:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, -1, 0):
                        game.current_piece['x'] -= 1
                elif event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, 1, 0):
                        game.current_piece['x'] += 1
                elif event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1):
                        game.current_piece['y'] += 1
                elif event.key == pygame.K_UP:
                    old_rotation = game.current_piece['rotation']
                    old_shape = game.current_piece['shape']
                    game.rotate_piece(game.current_piece)
                    if not game.valid_move(game.current_piece, 0, 0):
                        game.current_piece['rotation'] = old_rotation
                        game.current_piece['shape'] = old_shape
        
        game.update(dt)
        
        if game.game_over():
            font = pygame.font.Font(None, 72)
            game_over_text = font.render('GAME OVER', True, RED)
            screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            game = TetrisGame()
        
        game.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()

