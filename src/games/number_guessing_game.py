import random
import sys
import time

class NumberGuessingGame:
    def __init__(self):
        self.min_number = 1
        self.max_number = 100
        self.max_attempts = 10
        self.secret_number = None
        self.attempts = 0
        self.guess_history = []
        
    def set_difficulty(self):
        print("\n=== Choose Difficulty ===")
        print("1. Easy (1-50, 12 attempts)")
        print("2. Medium (1-100, 10 attempts)")
        print("3. Hard (1-200, 8 attempts)")
        print("4. Expert (1-500, 6 attempts)")
        print("5. Custom")
        
        while True:
            choice = input("\nSelect difficulty (1-5): ").strip()
            
            if choice == '1':
                self.min_number, self.max_number, self.max_attempts = 1, 50, 12
                break
            elif choice == '2':
                self.min_number, self.max_number, self.max_attempts = 1, 100, 10
                break
            elif choice == '3':
                self.min_number, self.max_number, self.max_attempts = 1, 200, 8
                break
            elif choice == '4':
                self.min_number, self.max_number, self.max_attempts = 1, 500, 6
                break
            elif choice == '5':
                self.custom_difficulty()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def custom_difficulty(self):
        while True:
            try:
                self.min_number = int(input("Enter minimum number: "))
                self.max_number = int(input("Enter maximum number: "))
                if self.max_number <= self.min_number:
                    print("Maximum must be greater than minimum!")
                    continue
                self.max_attempts = int(input("Enter maximum attempts: "))
                if self.max_attempts <= 0:
                    print("Must have at least 1 attempt!")
                    continue
                break
            except ValueError:
                print("Please enter valid numbers.")
    
    def start_new_game(self):
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        self.guess_history = []
        
        print(f"\n🎯 I'm thinking of a number between {self.min_number} and {self.max_number}")
        print(f"You have {self.max_attempts} attempts to guess it!")
        print("Type 'hint' for a hint, 'history' to see your guesses, or 'quit' to exit\n")
    
    def get_hint(self):
        hints = [
            f"The number is {'even' if self.secret_number % 2 == 0 else 'odd'}",
            f"The number is {'greater' if self.secret_number > (self.min_number + self.max_number) // 2 else 'less'} than {(self.min_number + self.max_number) // 2}",
            f"The sum of digits is {sum(int(digit) for digit in str(self.secret_number))}",
            f"The number {'is' if self.secret_number % 5 == 0 else 'is not'} divisible by 5",
            f"The number {'is' if self.secret_number % 3 == 0 else 'is not'} divisible by 3"
        ]
        
        # Don't repeat hints
        available_hints = [h for h in hints if h not in getattr(self, 'used_hints', [])]
        if not available_hints:
            return "No more hints available!"
        
        if not hasattr(self, 'used_hints'):
            self.used_hints = []
        
        hint = random.choice(available_hints)
        self.used_hints.append(hint)
        return f"💡 Hint: {hint}"
    
    def show_history(self):
        if not self.guess_history:
            return "No guesses yet!"
        
        history_str = "📊 Your guess history:\n"
        for i, (guess, feedback) in enumerate(self.guess_history, 1):
            history_str += f"{i:2d}. {guess:3d} - {feedback}\n"
        return history_str
    
    def get_feedback(self, guess):
        if guess == self.secret_number:
            return "🎉 Correct!"
        elif guess < self.secret_number:
            diff = self.secret_number - guess
            if diff <= 5:
                return "📈 Too low, but very close!"
            elif diff <= 15:
                return "📈 Too low, getting warm!"
            else:
                return "📈 Too low!"
        else:
            diff = guess - self.secret_number
            if diff <= 5:
                return "📉 Too high, but very close!"
            elif diff <= 15:
                return "📉 Too high, getting warm!"
            else:
                return "📉 Too high!"
    
    def calculate_score(self):
        # Score based on attempts used and difficulty
        base_score = 1000
        attempt_penalty = (self.attempts - 1) * 50
        difficulty_bonus = (self.max_number - self.min_number) // 10
        
        score = base_score - attempt_penalty + difficulty_bonus
        return max(score, 100)  # Minimum score of 100
    
    def play_round(self):
        while self.attempts < self.max_attempts:
            remaining = self.max_attempts - self.attempts
            prompt = f"Attempt {self.attempts + 1}/{self.max_attempts} ({remaining} left): "
            
            user_input = input(prompt).strip().lower()
            
            if user_input == 'quit':
                print(f"\nGiving up? The number was {self.secret_number}")
                return False
            elif user_input == 'hint':
                print(self.get_hint())
                continue
            elif user_input == 'history':
                print(self.show_history())
                continue
            
            try:
                guess = int(user_input)
                if guess < self.min_number or guess > self.max_number:
                    print(f"Please guess between {self.min_number} and {self.max_number}!")
                    continue
                
                self.attempts += 1
                feedback = self.get_feedback(guess)
                self.guess_history.append((guess, feedback))
                
                print(feedback)
                
                if guess == self.secret_number:
                    score = self.calculate_score()
                    print(f"\n🌟 Congratulations! You found it in {self.attempts} attempts!")
                    print(f"Your score: {score} points")
                    return True
                
            except ValueError:
                print("Please enter a valid number (or 'hint', 'history', 'quit')")
        
        print(f"\n💥 Game Over! You've used all {self.max_attempts} attempts.")
        print(f"The secret number was: {self.secret_number}")
        return False
    
    def show_statistics(self, games_played, games_won, total_attempts):
        if games_played == 0:
            return
        
        win_rate = (games_won / games_played) * 100
        avg_attempts = total_attempts / games_won if games_won > 0 else 0
        
        print(f"\n📈 Your Statistics:")
        print(f"Games played: {games_played}")
        print(f"Games won: {games_won}")
        print(f"Win rate: {win_rate:.1f}%")
        if games_won > 0:
            print(f"Average attempts per win: {avg_attempts:.1f}")
    
    def play(self):
        print("🎲 Welcome to the Number Guessing Game! 🎲")
        print("I'll think of a number and you try to guess it!")
        
        games_played = 0
        games_won = 0
        total_attempts = 0
        
        while True:
            self.set_difficulty()
            self.start_new_game()
            
            games_played += 1
            won = self.play_round()
            
            if won:
                games_won += 1
                total_attempts += self.attempts
            
            self.show_statistics(games_played, games_won, total_attempts)
            
            while True:
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("\nThanks for playing! 👋")
                    return
                else:
                    print("Please enter 'y' or 'n'")

class MultiplayerGuessingGame(NumberGuessingGame):
    def __init__(self):
        super().__init__()
        self.players = []
        self.current_player = 0
        self.player_attempts = {}
    
    def setup_players(self):
        while True:
            try:
                num_players = int(input("How many players? (2-6): "))
                if 2 <= num_players <= 6:
                    break
                else:
                    print("Please enter between 2 and 6 players.")
            except ValueError:
                print("Please enter a valid number.")
        
        self.players = []
        for i in range(num_players):
            name = input(f"Enter name for player {i+1}: ").strip()
            if not name:
                name = f"Player {i+1}"
            self.players.append(name)
            self.player_attempts[name] = 0
    
    def play_multiplayer(self):
        print("\n🎲 Multiplayer Number Guessing Game! 🎲")
        print("Players take turns guessing. First to guess correctly wins!")
        
        self.setup_players()
        self.set_difficulty()
        self.start_new_game()
        
        print(f"\nPlayers: {', '.join(self.players)}")
        print("Good luck everyone!\n")
        
        while True:
            current_player_name = self.players[self.current_player]
            print(f"\n{current_player_name}'s turn:")
            
            user_input = input(f"{current_player_name}, enter your guess: ").strip().lower()
            
            if user_input == 'quit':
                print(f"\n{current_player_name} quit. Game over!")
                print(f"The number was {self.secret_number}")
                return
            
            try:
                guess = int(user_input)
                if guess < self.min_number or guess > self.max_number:
                    print(f"Please guess between {self.min_number} and {self.max_number}!")
                    continue
                
                self.player_attempts[current_player_name] += 1
                feedback = self.get_feedback(guess)
                print(f"{current_player_name}: {feedback}")
                
                if guess == self.secret_number:
                    print(f"\n🎉 {current_player_name} wins!")
                    print(f"Found it in {self.player_attempts[current_player_name]} attempts!")
                    
                    # Show all player attempts
                    print("\nFinal attempts:")
                    for player in self.players:
                        print(f"{player}: {self.player_attempts[player]} attempts")
                    return
                
                # Next player's turn
                self.current_player = (self.current_player + 1) % len(self.players)
                
            except ValueError:
                print("Please enter a valid number.")

def main():
    while True:
        print("\n=== NUMBER GUESSING GAME ===")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. Quit")
        
        choice = input("\nChoose game mode (1-3): ").strip()
        
        if choice == '1':
            game = NumberGuessingGame()
            game.play()
        elif choice == '2':
            game = MultiplayerGuessingGame()
            game.play_multiplayer()
        elif choice == '3':
            print("Thanks for playing! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye! 👋")
        sys.exit()

