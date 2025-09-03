import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 5
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        self.speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off top and bottom
        if self.y <= 0 or self.y >= HEIGHT - BALL_SIZE:
            self.speed_y = -self.speed_y
            
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        self.speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, BALL_SIZE, BALL_SIZE))

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        
    def move(self):
        self.y += self.speed
        
        # Keep paddle on screen
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - PADDLE_HEIGHT:
            self.y = HEIGHT - PADDLE_HEIGHT
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

class PongGame:
    def __init__(self):
        self.ball = Ball()
        self.player1 = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.player2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 74)
        
    def handle_collisions(self):
        ball_rect = pygame.Rect(self.ball.x, self.ball.y, BALL_SIZE, BALL_SIZE)
        
        # Check collision with paddles
        if ball_rect.colliderect(self.player1.get_rect()):
            if self.ball.speed_x < 0:  # Only bounce if ball is moving towards paddle
                self.ball.speed_x = -self.ball.speed_x
                # Add some randomness to the bounce
                self.ball.speed_y += random.randint(-2, 2)
                
        if ball_rect.colliderect(self.player2.get_rect()):
            if self.ball.speed_x > 0:  # Only bounce if ball is moving towards paddle
                self.ball.speed_x = -self.ball.speed_x
                # Add some randomness to the bounce
                self.ball.speed_y += random.randint(-2, 2)
                
    def check_score(self):
        if self.ball.x < 0:
            self.score2 += 1
            self.ball.reset()
        elif self.ball.x > WIDTH:
            self.score1 += 1
            self.ball.reset()
            
    def ai_player(self):
        # Simple AI for player 2
        paddle_center = self.player2.y + PADDLE_HEIGHT // 2
        ball_center = self.ball.y + BALL_SIZE // 2
        
        if paddle_center < ball_center - 10:
            self.player2.speed = PADDLE_SPEED
        elif paddle_center > ball_center + 10:
            self.player2.speed = -PADDLE_SPEED
        else:
            self.player2.speed = 0
            
    def update(self):
        self.ball.move()
        self.player1.move()
        self.player2.move()
        self.handle_collisions()
        self.check_score()
        self.ai_player()
        
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw center line
        for i in range(0, HEIGHT, 20):
            if i % 40 == 0:
                pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, i, 4, 10))
        
        # Draw game objects
        self.ball.draw(screen)
        self.player1.draw(screen)
        self.player2.draw(screen)
        
        # Draw scores
        score1_text = self.font.render(str(self.score1), True, WHITE)
        score2_text = self.font.render(str(self.score2), True, WHITE)
        
        screen.blit(score1_text, (WIDTH // 4, 50))
        screen.blit(score2_text, (WIDTH * 3 // 4, 50))
        
        # Draw instructions
        font_small = pygame.font.Font(None, 36)
        instruction_text = font_small.render('W/S to move paddle', True, WHITE)
        screen.blit(instruction_text, (10, HEIGHT - 40))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    game = PongGame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.player1.speed = -PADDLE_SPEED
        elif keys[pygame.K_s]:
            game.player1.speed = PADDLE_SPEED
        else:
            game.player1.speed = 0
            
        # Optional: Two player mode
        if keys[pygame.K_UP]:
            game.player2.speed = -PADDLE_SPEED
        elif keys[pygame.K_DOWN]:
            game.player2.speed = PADDLE_SPEED
        # Comment out the ai_player() call in update() for two player mode
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

