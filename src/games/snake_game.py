import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Moving right initially
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
        
        # Check for self collision
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True

    def change_direction(self, new_direction):
        # Prevent moving in opposite direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow_snake(self):
        self.grow = True

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
            color = GREEN if i == 0 else DARK_GREEN  # Head is brighter
            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        x, y = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - Score: 0")
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        if not self.snake.move():
            return False  # Game over
        
        # Check if snake ate food
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.score += 10
            pygame.display.set_caption(f"Snake Game - Score: {self.score}")
            
            # Generate new food position (make sure it's not on snake)
            while self.food.position in self.snake.body:
                self.food.position = self.food.generate_position()
        
        return True

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def game_over_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER!", True, WHITE)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

    def wait_for_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False

    def run(self):
        running = True
        game_active = True
        
        while running:
            if game_active:
                running = self.handle_events()
                if running:
                    game_active = self.update()
                    self.draw()
                    self.clock.tick(10)  # Control game speed
                
                if not game_active:
                    self.game_over_screen()
            else:
                # Game over state
                restart = self.wait_for_restart()
                if restart:
                    # Reset game
                    self.snake = Snake()
                    self.food = Food()
                    self.score = 0
                    pygame.display.set_caption("Snake Game - Score: 0")
                    game_active = True
                else:
                    running = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("Starting Snake Game!")
    print("Controls:")
    print("- Arrow keys to move")
    print("- ESC to quit")
    print("- SPACE to restart after game over")
    print()
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        pygame.quit()
        sys.exit()

