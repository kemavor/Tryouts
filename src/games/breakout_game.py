import random
import sys
import os
import time
import threading
from threading import Lock

class BreakoutGame:
    def __init__(self):
        self.width = 60
        self.height = 20
        self.paddle_width = 8
        self.paddle_pos = self.width // 2 - self.paddle_width // 2
        self.ball_x = self.width // 2
        self.ball_y = self.height - 3
        self.ball_dx = 1
        self.ball_dy = -1
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_running = False
        self.game_over = False
        self.lock = Lock()
        self.last_move_time = 0
        self.move_delay = 0.1  # Seconds between moves
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def setup_bricks(self, pattern='classic'):
        self.bricks = []
        
        if pattern == 'classic':
            # Classic brick pattern
            for row in range(3, 8):
                for col in range(5, self.width - 5):
                    if col % 2 == 0:  # Create gaps
                        self.bricks.append((col, row))
        
        elif pattern == 'pyramid':
            # Pyramid pattern
            for row in range(3, 8):
                start = self.width // 2 - (8 - row)
                end = self.width // 2 + (8 - row)
                for col in range(max(5, start), min(self.width - 5, end)):
                    if col % 2 == 0:
                        self.bricks.append((col, row))
        
        elif pattern == 'diamond':
            # Diamond pattern
            center = self.width // 2
            for row in range(2, 10):
                width = abs(6 - row) + 2
                for col in range(center - width, center + width):
                    if col % 2 == 0 and 5 < col < self.width - 5:
                        self.bricks.append((col, row))
        
        elif pattern == 'walls':
            # Side walls pattern
            for row in range(3, 12):
                for col in [8, 10, self.width - 11, self.width - 9]:
                    self.bricks.append((col, row))
            # Top section
            for row in range(3, 6):
                for col in range(15, self.width - 15):
                    if col % 3 == 0:
                        self.bricks.append((col, row))
    
    def draw_game(self):
        with self.lock:
            self.clear_screen()
            
            # Create game field
            field = [[' ' for _ in range(self.width)] for _ in range(self.height)]
            
            # Draw borders
            for i in range(self.width):
                field[0][i] = '═'  # Top border
                field[self.height-1][i] = '═'  # Bottom border
            for i in range(self.height):
                field[i][0] = '║'  # Left border
                field[i][self.width-1] = '║'  # Right border
            
            # Draw corners
            field[0][0] = '╔'
            field[0][self.width-1] = '╗'
            field[self.height-1][0] = '╚'
            field[self.height-1][self.width-1] = '╝'
            
            # Draw bricks
            for brick_x, brick_y in self.bricks:
                if 0 <= brick_x < self.width and 0 <= brick_y < self.height:
                    field[brick_y][brick_x] = '█'  # Full block
            
            # Draw paddle
            for i in range(self.paddle_width):
                paddle_x = self.paddle_pos + i
                if 0 <= paddle_x < self.width:
                    field[self.height-2][paddle_x] = '▄'  # Lower half block
            
            # Draw ball
            if 0 <= int(self.ball_x) < self.width and 0 <= int(self.ball_y) < self.height:
                field[int(self.ball_y)][int(self.ball_x)] = '●'  # Circle
            
            # Print the field
            print(f"🎮 BREAKOUT - Level {self.level} 🎮")
            print(f"Score: {self.score:06d} | Lives: {'♥' * self.lives} | Bricks: {len(self.bricks)}")
            print()
            
            for row in field:
                print(''.join(row))
            
            print()
            print("Controls: A/D or ←/→ to move paddle, Q to quit")
            print("Press any key and Enter to move, or just Enter to continue")
    
    def move_ball(self):
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Ball collision with walls
        if self.ball_x <= 1:
            self.ball_x = 1
            self.ball_dx = abs(self.ball_dx)
        elif self.ball_x >= self.width - 2:
            self.ball_x = self.width - 2
            self.ball_dx = -abs(self.ball_dx)
        
        if self.ball_y <= 1:
            self.ball_y = 1
            self.ball_dy = abs(self.ball_dy)
        
        # Ball collision with paddle
        if (self.ball_y >= self.height - 3 and 
            self.paddle_pos <= self.ball_x <= self.paddle_pos + self.paddle_width):
            self.ball_dy = -abs(self.ball_dy)
            # Add some angle based on where ball hits paddle
            hit_pos = (self.ball_x - self.paddle_pos) / self.paddle_width
            self.ball_dx = (hit_pos - 0.5) * 2  # Range from -1 to 1
        
        # Ball collision with bricks
        ball_grid_x = int(self.ball_x)
        ball_grid_y = int(self.ball_y)
        
        hit_brick = None
        for brick in self.bricks:
            brick_x, brick_y = brick
            if brick_x == ball_grid_x and brick_y == ball_grid_y:
                hit_brick = brick
                break
        
        if hit_brick:
            self.bricks.remove(hit_brick)
            self.score += 10
            self.ball_dy = -self.ball_dy  # Reverse ball direction
        
        # Ball goes below paddle (lose life)
        if self.ball_y >= self.height - 1:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset ball position
                self.ball_x = self.width // 2
                self.ball_y = self.height - 3
                self.ball_dx = random.choice([-1, 1])
                self.ball_dy = -1
        
        # Check win condition
        if not self.bricks:
            self.level += 1
            self.score += 100 * self.level
            if self.level <= 4:
                patterns = ['classic', 'pyramid', 'diamond', 'walls']
                self.setup_bricks(patterns[self.level - 1])
                # Reset ball
                self.ball_x = self.width // 2
                self.ball_y = self.height - 3
                self.ball_dx = random.choice([-1, 1])
                self.ball_dy = -1
            else:
                self.game_over = True  # Game won!
    
    def move_paddle(self, direction):
        current_time = time.time()
        if current_time - self.last_move_time < self.move_delay:
            return
        
        self.last_move_time = current_time
        
        if direction == 'left' and self.paddle_pos > 1:
            self.paddle_pos -= 2
        elif direction == 'right' and self.paddle_pos < self.width - self.paddle_width - 1:
            self.paddle_pos += 2
    
    def get_input_with_timeout(self, timeout=0.15):
        """Get input with timeout for responsive gameplay"""
        import select
        import sys
        
        if os.name == 'nt':  # Windows
            import msvcrt
            start_time = time.time()
            while time.time() - start_time < timeout:
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode('utf-8').lower()
                    # Clear any remaining characters
                    while msvcrt.kbhit():
                        msvcrt.getch()
                    return char
                time.sleep(0.01)
            return None
        else:  # Unix/Linux/Mac
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                line = sys.stdin.readline().strip().lower()
                return line[0] if line else None
            return None
    
    def play_turn_based(self):
        """Turn-based version for better compatibility"""
        print("🎮 Welcome to Breakout! 🎮")
        print("Turn-based mode: Make your move each turn!")
        print("Commands: 'a' or 'left' to move left, 'd' or 'right' to move right")
        print("Just press Enter to let the ball move without moving paddle")
        input("\nPress Enter to start...")
        
        self.setup_bricks('classic')
        
        while not self.game_over:
            self.draw_game()
            
            if self.lives <= 0:
                print(f"\n😞 GAME OVER! Final Score: {self.score}")
                break
            
            if not self.bricks and self.level > 4:
                print(f"\n🎆 CONGRATULATIONS! You completed all levels!")
                print(f"Final Score: {self.score}")
                break
            
            # Get player input
            try:
                move = input("\nYour move: ").strip().lower()
                
                if move in ['q', 'quit']:
                    print("Thanks for playing!")
                    break
                elif move in ['a', 'left', '←']:
                    self.move_paddle('left')
                elif move in ['d', 'right', '→']:
                    self.move_paddle('right')
                # For empty input, just move the ball
                
                self.move_ball()
                
            except KeyboardInterrupt:
                print("\nGame interrupted!")
                break
    
    def play_real_time(self):
        """Real-time version (may not work on all systems)"""
        print("🎮 Welcome to Breakout - Real Time Mode! 🎮")
        print("Use A/D keys to move paddle")
        print("This mode updates automatically - press Q to quit")
        input("\nPress Enter to start...")
        
        self.setup_bricks('classic')
        self.game_running = True
        
        # Game loop
        while self.game_running and not self.game_over:
            self.draw_game()
            
            if self.lives <= 0:
                print(f"\n😞 GAME OVER! Final Score: {self.score}")
                break
            
            if not self.bricks and self.level > 4:
                print(f"\n🎆 CONGRATULATIONS! You completed all levels!")
                print(f"Final Score: {self.score}")
                break
            
            # Get input with timeout
            key = self.get_input_with_timeout(0.2)
            
            if key:
                if key in ['q', 'quit']:
                    self.game_running = False
                    break
                elif key in ['a', 'left']:
                    self.move_paddle('left')
                elif key in ['d', 'right']:
                    self.move_paddle('right')
            
            self.move_ball()
            time.sleep(0.1)  # Game speed
    
    def show_demo(self):
        """Show a demo of the game"""
        print("🎮 Breakout Demo 🎮")
        print("Watch the AI play!")
        input("Press Enter to start demo...")
        
        self.setup_bricks('pyramid')
        
        for _ in range(50):  # 50 demo moves
            self.draw_game()
            
            # Simple AI: move paddle towards ball
            paddle_center = self.paddle_pos + self.paddle_width // 2
            if self.ball_x < paddle_center:
                self.move_paddle('left')
            elif self.ball_x > paddle_center:
                self.move_paddle('right')
            
            self.move_ball()
            time.sleep(0.3)
            
            if not self.bricks or self.lives <= 0:
                break
        
        print("\nDemo finished!")
    
    def calculate_high_score(self):
        # Bonus points for lives remaining and level reached
        life_bonus = self.lives * 50
        level_bonus = self.level * 200
        return self.score + life_bonus + level_bonus

def main():
    while True:
        print("\n" + "="*50)
        print("🎮 BREAKOUT GAME 🎮")
        print("="*50)
        print("Break all the bricks with your ball!")
        print("Control the paddle to keep the ball in play.")
        print()
        print("1. Play Turn-Based Mode (Recommended)")
        print("2. Play Real-Time Mode (Advanced)")
        print("3. Watch Demo")
        print("4. How to Play")
        print("5. Quit")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == '1':
            game = BreakoutGame()
            game.play_turn_based()
            
            if game.score > 0:
                final_score = game.calculate_high_score()
                print(f"\n🏆 Game Statistics:")
                print(f"Levels completed: {game.level - 1}")
                print(f"Final score: {final_score}")
                print(f"Lives remaining: {game.lives}")
        
        elif choice == '2':
            game = BreakoutGame()
            try:
                game.play_real_time()
            except Exception as e:
                print(f"\nReal-time mode not supported on this system.")
                print(f"Please use turn-based mode instead.")
                continue
            
            if game.score > 0:
                final_score = game.calculate_high_score()
                print(f"\n🏆 Game Statistics:")
                print(f"Levels completed: {game.level - 1}")
                print(f"Final score: {final_score}")
                print(f"Lives remaining: {game.lives}")
        
        elif choice == '3':
            game = BreakoutGame()
            game.show_demo()
        
        elif choice == '4':
            print("\n📚 HOW TO PLAY:")
            print("- Use your paddle to bounce the ball")
            print("- Hit all bricks to complete the level")
            print("- Don't let the ball fall below your paddle")
            print("- You have 3 lives to complete all levels")
            print("- Each brick gives 10 points")
            print("- Level completion gives bonus points")
            print("- 4 different levels with unique patterns")
            print("\nCONTROLS:")
            print("- Turn-based: Type 'a' or 'd' and press Enter")
            print("- Real-time: Press 'a' or 'd' keys directly")
            print("- 'q' to quit anytime")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            print("Thanks for playing Breakout! 🎮")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye! 🎮")
        sys.exit()

