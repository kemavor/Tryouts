import random
import sys
import os
import time

class MemoryMatchGame:
    def __init__(self):
        self.symbols = ['🐱', '🐶', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', 
                       '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🐣',
                       '🦄', '🐝', '🦋', '🐌', '🐛', '🐜', '🐞', '🦗',
                       '🌟', '⭐', '🔥', '💎', '🎵', '🎨', '🎭', '🎪']
        
        self.board = []
        self.revealed = []
        self.matched = []
        self.rows = 4
        self.cols = 4
        self.attempts = 0
        self.matches = 0
        self.start_time = 0
        self.game_won = False
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def select_difficulty(self):
        print("\n=== Choose Difficulty ===")
        print("1. Easy (4x4 grid, 8 pairs)")
        print("2. Medium (4x6 grid, 12 pairs)")
        print("3. Hard (6x6 grid, 18 pairs)")
        print("4. Expert (6x8 grid, 24 pairs)")
        print("5. Custom")
        
        while True:
            choice = input("\nSelect difficulty (1-5): ").strip()
            
            if choice == '1':
                self.rows, self.cols = 4, 4
                break
            elif choice == '2':
                self.rows, self.cols = 4, 6
                break
            elif choice == '3':
                self.rows, self.cols = 6, 6
                break
            elif choice == '4':
                self.rows, self.cols = 6, 8
                break
            elif choice == '5':
                self.custom_difficulty()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def custom_difficulty(self):
        while True:
            try:
                self.rows = int(input("Enter number of rows (3-8): "))
                self.cols = int(input("Enter number of columns (3-8): "))
                
                if not (3 <= self.rows <= 8 and 3 <= self.cols <= 8):
                    print("Rows and columns must be between 3 and 8.")
                    continue
                
                total_cards = self.rows * self.cols
                if total_cards % 2 != 0:
                    print("Total cards must be even (for pairs). Try different dimensions.")
                    continue
                
                break
            except ValueError:
                print("Please enter valid numbers.")
    
    def setup_board(self):
        total_cards = self.rows * self.cols
        num_pairs = total_cards // 2
        
        # Select random symbols for this game
        selected_symbols = random.sample(self.symbols, num_pairs)
        
        # Create pairs
        card_symbols = selected_symbols * 2
        random.shuffle(card_symbols)
        
        # Create board
        self.board = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                index = i * self.cols + j
                row.append(card_symbols[index])
            self.board.append(row)
        
        # Initialize game state
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.matched = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.attempts = 0
        self.matches = 0
        self.game_won = False
        self.start_time = time.time()
    
    def display_board(self, show_all=False, temp_revealed=None):
        self.clear_screen()
        print("🧠 MEMORY MATCH GAME 🧠")
        print("=" * 40)
        print(f"Matches: {self.matches}/{(self.rows * self.cols) // 2}")
        print(f"Attempts: {self.attempts}")
        
        if self.start_time > 0:
            elapsed = int(time.time() - self.start_time)
            print(f"Time: {elapsed // 60:02d}:{elapsed % 60:02d}")
        
        print()
        
        # Column headers
        print("   ", end="")
        for j in range(self.cols):
            print(f"{j+1:^4}", end="")
        print()
        
        # Board
        for i in range(self.rows):
            print(f"{i+1:2} ", end="")
            for j in range(self.cols):
                if show_all or self.matched[i][j] or self.revealed[i][j]:
                    print(f"{self.board[i][j]:^4}", end="")
                elif temp_revealed and (i, j) in temp_revealed:
                    print(f"{self.board[i][j]:^4}", end="")
                else:
                    print("🔳", end=" ")
            print()
        
        print()
    
    def get_card_position(self):
        while True:
            try:
                pos_input = input("Enter card position (row,col) or 'q' to quit: ").strip().lower()
                
                if pos_input == 'q':
                    return None, None
                
                if ',' in pos_input:
                    row, col = map(int, pos_input.split(','))
                else:
                    row, col = map(int, pos_input.split())
                
                # Convert to 0-based indexing
                row -= 1
                col -= 1
                
                if not (0 <= row < self.rows and 0 <= col < self.cols):
                    print(f"Position must be between (1,1) and ({self.rows},{self.cols}).")
                    continue
                
                if self.matched[row][col]:
                    print("That card is already matched. Choose another.")
                    continue
                
                if self.revealed[row][col]:
                    print("That card is already revealed. Choose another.")
                    continue
                
                return row, col
                
            except (ValueError, IndexError):
                print("Please enter valid coordinates (e.g., '2,3' or '2 3').")
    
    def reveal_card(self, row, col):
        self.revealed[row][col] = True
    
    def hide_card(self, row, col):
        self.revealed[row][col] = False
    
    def match_cards(self, row1, col1, row2, col2):
        self.matched[row1][col1] = True
        self.matched[row2][col2] = True
        self.matches += 1
    
    def check_win(self):
        total_pairs = (self.rows * self.cols) // 2
        return self.matches == total_pairs
    
    def calculate_score(self):
        # Score based on attempts, time, and difficulty
        total_pairs = (self.rows * self.cols) // 2
        perfect_attempts = total_pairs
        elapsed_time = int(time.time() - self.start_time)
        
        # Base score
        base_score = 1000
        
        # Attempt penalty
        attempt_penalty = max(0, (self.attempts - perfect_attempts) * 50)
        
        # Time penalty (1 point per second over 2 minutes)
        time_penalty = max(0, (elapsed_time - 120) * 1)
        
        # Difficulty bonus
        difficulty_bonus = total_pairs * 20
        
        score = base_score - attempt_penalty - time_penalty + difficulty_bonus
        return max(score, 100)
    
    def show_peek(self, duration=2):
        """Show all cards briefly at the start"""
        print("\n👀 Get ready! Here's a quick peek at all the cards...")
        input("Press Enter to continue...")
        
        self.display_board(show_all=True)
        print(f"\nMemorizing time! Cards will be hidden in {duration} seconds...")
        time.sleep(duration)
        
        self.display_board()
        print("Now find the matching pairs!")
    
    def play_round(self):
        # Show peek at the beginning
        self.show_peek()
        
        while not self.game_won:
            self.display_board()
            
            print("Find two matching cards!")
            print("Commands: 'row,col' to select card, 'q' to quit")
            
            # Get first card
            print("\nSelect first card:")
            row1, col1 = self.get_card_position()
            if row1 is None:
                return False
            
            self.reveal_card(row1, col1)
            self.display_board()
            
            # Get second card
            print("\nSelect second card:")
            row2, col2 = self.get_card_position()
            if row2 is None:
                return False
            
            # Check if same card
            if row1 == row2 and col1 == col2:
                print("You can't select the same card twice!")
                self.hide_card(row1, col1)
                input("Press Enter to continue...")
                continue
            
            self.reveal_card(row2, col2)
            self.attempts += 1
            
            # Show both cards
            self.display_board()
            
            # Check for match
            if self.board[row1][col1] == self.board[row2][col2]:
                print(f"\n🎉 Match found! {self.board[row1][col1]} = {self.board[row2][col2]}")
                self.match_cards(row1, col1, row2, col2)
                
                if self.check_win():
                    self.game_won = True
                    self.display_board()
                    elapsed_time = int(time.time() - self.start_time)
                    score = self.calculate_score()
                    
                    print(f"\n🏆 CONGRATULATIONS! YOU WON! 🏆")
                    print(f"Completed in {self.attempts} attempts")
                    print(f"Time: {elapsed_time // 60:02d}:{elapsed_time % 60:02d}")
                    print(f"Score: {score} points")
                    
                    # Performance rating
                    total_pairs = (self.rows * self.cols) // 2
                    if self.attempts == total_pairs:
                        print("🌟 PERFECT GAME! Amazing memory!")
                    elif self.attempts <= total_pairs * 1.5:
                        print("⭐ EXCELLENT! Great job!")
                    elif self.attempts <= total_pairs * 2:
                        print("👍 GOOD! Well done!")
                    else:
                        print("👌 COMPLETED! Keep practicing!")
                else:
                    print(f"Great! {self.matches} pairs found, {(self.rows * self.cols) // 2 - self.matches} to go!")
            else:
                print(f"\n❌ No match: {self.board[row1][col1]} ≠ {self.board[row2][col2]}")
                input("\nPress Enter to continue...")
                self.hide_card(row1, col1)
                self.hide_card(row2, col2)
        
        return True
    
    def show_statistics(self, games_played, games_won, total_time, best_score):
        if games_played > 0:
            avg_time = total_time / games_won if games_won > 0 else 0
            win_rate = (games_won / games_played) * 100
            
            print(f"\n📊 Statistics:")
            print(f"Games played: {games_played}")
            print(f"Games completed: {games_won}")
            print(f"Completion rate: {win_rate:.1f}%")
            if games_won > 0:
                print(f"Average completion time: {int(avg_time // 60):02d}:{int(avg_time % 60):02d}")
                print(f"Best score: {best_score}")
    
    def play(self):
        print("🧠 Welcome to Memory Match! 🧠")
        print("Find all the matching pairs of cards!")
        print("You'll get a quick peek at all cards at the start.")
        
        games_played = 0
        games_won = 0
        total_time = 0
        best_score = 0
        
        while True:
            self.select_difficulty()
            self.setup_board()
            
            games_played += 1
            completed = self.play_round()
            
            if not completed:
                print("\nThanks for playing!")
                break
            
            if self.game_won:
                games_won += 1
                game_time = time.time() - self.start_time
                total_time += game_time
                score = self.calculate_score()
                best_score = max(best_score, score)
            
            self.show_statistics(games_played, games_won, total_time, best_score)
            
            # Ask to play again
            while True:
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("\nThanks for playing Memory Match! 🧠")
                    return
                else:
                    print("Please enter 'y' or 'n'")

class TimeAttackMode(MemoryMatchGame):
    """Time-limited version of Memory Match"""
    
    def __init__(self):
        super().__init__()
        self.time_limit = 120  # 2 minutes default
    
    def select_time_limit(self):
        print("\n=== Choose Time Limit ===")
        print("1. Sprint (1 minute)")
        print("2. Quick (2 minutes)")
        print("3. Standard (3 minutes)")
        print("4. Relaxed (5 minutes)")
        print("5. Custom")
        
        while True:
            choice = input("\nSelect time limit (1-5): ").strip()
            
            if choice == '1':
                self.time_limit = 60
                break
            elif choice == '2':
                self.time_limit = 120
                break
            elif choice == '3':
                self.time_limit = 180
                break
            elif choice == '4':
                self.time_limit = 300
                break
            elif choice == '5':
                try:
                    self.time_limit = int(input("Enter time limit in seconds: "))
                    if self.time_limit <= 0:
                        print("Time limit must be positive.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Invalid choice. Please try again.")
    
    def is_time_up(self):
        return time.time() - self.start_time >= self.time_limit
    
    def display_board(self, show_all=False, temp_revealed=None):
        super().display_board(show_all, temp_revealed)
        
        # Show remaining time
        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            print(f"⏰ Time remaining: {mins:02d}:{secs:02d}")
        else:
            print("⏰ TIME'S UP!")
        print()
    
    def play_time_attack(self):
        print("\n⏰ TIME ATTACK MODE! ⏰")
        print(f"You have {self.time_limit} seconds to find all pairs!")
        
        self.select_difficulty()
        self.select_time_limit()
        self.setup_board()
        
        # Show peek but shorter in time attack
        self.show_peek(duration=1)
        
        while not self.game_won and not self.is_time_up():
            self.display_board()
            
            if self.is_time_up():
                break
            
            print("Find two matching cards quickly!")
            
            # Get first card
            print("\nSelect first card:")
            row1, col1 = self.get_card_position()
            if row1 is None or self.is_time_up():
                break
            
            self.reveal_card(row1, col1)
            self.display_board()
            
            if self.is_time_up():
                break
            
            # Get second card
            print("\nSelect second card:")
            row2, col2 = self.get_card_position()
            if row2 is None or self.is_time_up():
                break
            
            # Check if same card
            if row1 == row2 and col1 == col2:
                print("You can't select the same card twice!")
                self.hide_card(row1, col1)
                continue
            
            self.reveal_card(row2, col2)
            self.attempts += 1
            
            # Show both cards
            self.display_board()
            
            if self.is_time_up():
                break
            
            # Check for match
            if self.board[row1][col1] == self.board[row2][col2]:
                print(f"\n🎉 Match found! {self.board[row1][col1]} = {self.board[row2][col2]}")
                self.match_cards(row1, col1, row2, col2)
                
                if self.check_win():
                    self.game_won = True
                    break
                
                time.sleep(0.5)  # Brief pause to show the match
            else:
                print(f"\n❌ No match: {self.board[row1][col1]} ≠ {self.board[row2][col2]}")
                time.sleep(1)  # Brief pause to memorize
                self.hide_card(row1, col1)
                self.hide_card(row2, col2)
        
        # Game over
        self.display_board(show_all=True)
        
        if self.game_won:
            elapsed_time = int(time.time() - self.start_time)
            time_bonus = max(0, self.time_limit - elapsed_time) * 10
            score = self.calculate_score() + time_bonus
            
            print(f"\n🏆 TIME ATTACK COMPLETED! 🏆")
            print(f"Completed in {elapsed_time} seconds")
            print(f"Time bonus: {time_bonus} points")
            print(f"Final score: {score} points")
        else:
            print(f"\n⏰ TIME'S UP! ⏰")
            print(f"You found {self.matches} out of {(self.rows * self.cols) // 2} pairs")
            print(f"Attempts: {self.attempts}")
        
        return self.game_won

def main():
    while True:
        print("\n" + "="*40)
        print("🧠 MEMORY MATCH GAME 🧠")
        print("="*40)
        print("1. Classic Mode")
        print("2. Time Attack Mode")
        print("3. Quit")
        
        choice = input("\nChoose game mode (1-3): ").strip()
        
        if choice == '1':
            game = MemoryMatchGame()
            game.play()
        elif choice == '2':
            game = TimeAttackMode()
            game.play_time_attack()
        elif choice == '3':
            print("Thanks for playing! 🧠")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye! 🧠")
        sys.exit()

