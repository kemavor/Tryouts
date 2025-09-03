import random
import sys
import os

class HangmanGame:
    def __init__(self):
        self.word_categories = {
            'animals': ['elephant', 'giraffe', 'penguin', 'dolphin', 'butterfly', 'kangaroo', 'rhinoceros', 
                       'octopus', 'chimpanzee', 'crocodile', 'flamingo', 'hedgehog', 'jaguar', 'koala'],
            'countries': ['australia', 'brazil', 'canada', 'denmark', 'egypt', 'france', 'germany', 
                         'hungary', 'iceland', 'japan', 'kenya', 'luxembourg', 'morocco', 'norway'],
            'foods': ['pizza', 'hamburger', 'spaghetti', 'chocolate', 'strawberry', 'pineapple', 
                     'sandwich', 'pancake', 'avocado', 'broccoli', 'cinnamon', 'doughnut'],
            'movies': ['titanic', 'avatar', 'inception', 'gladiator', 'casablanca', 'matrix', 
                      'superman', 'batman', 'spiderman', 'frozen', 'shrek', 'finding'],
            'sports': ['basketball', 'football', 'tennis', 'swimming', 'volleyball', 'baseball', 
                      'hockey', 'cricket', 'badminton', 'cycling', 'boxing', 'wrestling'],
            'technology': ['computer', 'smartphone', 'internet', 'software', 'hardware', 'keyboard', 
                          'monitor', 'printer', 'scanner', 'webcam', 'bluetooth', 'wireless']
        }
        
        self.hangman_stages = [
            """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
            """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
            """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
            r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
            r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
""",
            r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
""",
            r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
"""
        ]
        
        self.reset_game()
    
    def reset_game(self):
        self.word = ""
        self.category = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = len(self.hangman_stages) - 1
        self.game_won = False
        self.game_lost = False
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def choose_word(self, category=None):
        if category and category in self.word_categories:
            self.category = category
            self.word = random.choice(self.word_categories[category]).upper()
        else:
            self.category = random.choice(list(self.word_categories.keys()))
            self.word = random.choice(self.word_categories[self.category]).upper()
    
    def display_word(self):
        display = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        return display.strip()
    
    def display_hangman(self):
        return self.hangman_stages[self.wrong_guesses]
    
    def display_game_state(self):
        self.clear_screen()
        print("🎯 HANGMAN GAME 🎯")
        print("=" * 30)
        print(f"Category: {self.category.title()}")
        print(f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong_guesses}")
        print()
        print(self.display_hangman())
        print()
        print(f"Word: {self.display_word()}")
        print()
        
        if self.guessed_letters:
            correct_guesses = [letter for letter in self.guessed_letters if letter in self.word]
            wrong_guesses = [letter for letter in self.guessed_letters if letter not in self.word]
            
            if correct_guesses:
                print(f"✅ Correct letters: {', '.join(sorted(correct_guesses))}")
            if wrong_guesses:
                print(f"❌ Wrong letters: {', '.join(sorted(wrong_guesses))}")
            print()
    
    def get_guess(self):
        while True:
            guess = input("Enter a letter (or 'quit' to exit): ").strip().upper()
            
            if guess.lower() == 'quit':
                return None
            
            if len(guess) != 1:
                print("Please enter a single letter.")
                continue
            
            if not guess.isalpha():
                print("Please enter a valid letter.")
                continue
            
            if guess in self.guessed_letters:
                print(f"You already guessed '{guess}'. Try a different letter.")
                continue
            
            return guess
    
    def make_guess(self, letter):
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            print(f"🎉 Good guess! '{letter}' is in the word.")
            # Check if word is complete
            if all(letter in self.guessed_letters for letter in self.word):
                self.game_won = True
        else:
            self.wrong_guesses += 1
            print(f"😞 Sorry, '{letter}' is not in the word.")
            # Check if game is lost
            if self.wrong_guesses >= self.max_wrong_guesses:
                self.game_lost = True
        
        input("\nPress Enter to continue...")
    
    def get_hint(self):
        # Show a random letter that hasn't been guessed
        available_letters = [letter for letter in self.word if letter not in self.guessed_letters]
        if available_letters:
            hint_letter = random.choice(available_letters)
            return f"💡 Hint: The word contains the letter '{hint_letter}'"
        return "No more hints available!"
    
    def show_category_hint(self):
        hints = {
            'animals': "It's a living creature from the animal kingdom",
            'countries': "It's a nation or country in the world",
            'foods': "It's something you can eat or drink",
            'movies': "It's the title of a famous movie",
            'sports': "It's a sport or physical activity",
            'technology': "It's related to computers or modern technology"
        }
        return f"📚 Category hint: {hints.get(self.category, 'No hint available')}"
    
    def select_category(self):
        print("\n=== Choose a Category ===")
        categories = list(self.word_categories.keys())
        
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.title()}")
        print(f"{len(categories) + 1}. Random")
        
        while True:
            try:
                choice = int(input(f"\nSelect category (1-{len(categories) + 1}): "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                elif choice == len(categories) + 1:
                    return None  # Random
                else:
                    print(f"Please enter a number between 1 and {len(categories) + 1}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_difficulty(self):
        print("\n=== Choose Difficulty ===")
        print("1. Easy (8 wrong guesses allowed)")
        print("2. Medium (6 wrong guesses allowed) - Default")
        print("3. Hard (4 wrong guesses allowed)")
        print("4. Expert (3 wrong guesses allowed)")
        
        while True:
            choice = input("\nSelect difficulty (1-4) or Enter for default: ").strip()
            
            if choice == '' or choice == '2':
                self.max_wrong_guesses = 6
                break
            elif choice == '1':
                self.max_wrong_guesses = 8
                break
            elif choice == '3':
                self.max_wrong_guesses = 4
                break
            elif choice == '4':
                self.max_wrong_guesses = 3
                break
            else:
                print("Invalid choice. Please try again.")
    
    def play_round(self):
        while not self.game_won and not self.game_lost:
            self.display_game_state()
            
            # Show available commands
            print("Commands: letter to guess, 'hint' for hint, 'category' for category hint, 'quit' to exit")
            
            user_input = input("Your move: ").strip().lower()
            
            if user_input == 'quit':
                return False
            elif user_input == 'hint':
                print(self.get_hint())
                input("\nPress Enter to continue...")
                continue
            elif user_input == 'category':
                print(self.show_category_hint())
                input("\nPress Enter to continue...")
                continue
            elif len(user_input) == 1 and user_input.isalpha():
                letter = user_input.upper()
                if letter not in self.guessed_letters:
                    self.make_guess(letter)
                else:
                    print(f"You already guessed '{letter}'. Try a different letter.")
                    input("\nPress Enter to continue...")
            else:
                print("Please enter a single letter, 'hint', 'category', or 'quit'.")
                input("\nPress Enter to continue...")
        
        # Game over
        self.display_game_state()
        
        if self.game_won:
            print(f"🎉 Congratulations! You won!")
            print(f"The word was: {self.word}")
            print(f"You made {self.wrong_guesses} wrong guesses.")
        else:
            print(f"😵 Game Over! You lost!")
            print(f"The word was: {self.word}")
        
        return True
    
    def show_statistics(self, games_played, games_won):
        if games_played > 0:
            win_rate = (games_won / games_played) * 100
            print(f"\n📈 Statistics:")
            print(f"Games played: {games_played}")
            print(f"Games won: {games_won}")
            print(f"Win rate: {win_rate:.1f}%")
    
    def play(self):
        print("🎯 Welcome to Hangman! 🎯")
        print("Guess the word letter by letter before the drawing is complete!")
        
        games_played = 0
        games_won = 0
        
        while True:
            self.reset_game()
            
            # Game setup
            self.select_difficulty()
            category = self.select_category()
            self.choose_word(category)
            
            games_played += 1
            completed = self.play_round()
            
            if not completed:
                print("\nThanks for playing!")
                break
            
            if self.game_won:
                games_won += 1
            
            self.show_statistics(games_played, games_won)
            
            # Ask to play again
            while True:
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("\nThanks for playing Hangman! 👋")
                    return
                else:
                    print("Please enter 'y' or 'n'")

class WordHintGame(HangmanGame):
    """Enhanced version with word definitions and better hints"""
    
    def __init__(self):
        super().__init__()
        self.word_hints = {
            'ELEPHANT': "Large mammal with a trunk",
            'GIRAFFE': "Tallest animal with a long neck",
            'PENGUIN': "Black and white bird that can't fly but swims",
            'DOLPHIN': "Intelligent marine mammal",
            'AUSTRALIA': "Country that's also a continent",
            'BRAZIL': "Largest country in South America",
            'PIZZA': "Italian dish with cheese and toppings",
            'CHOCOLATE': "Sweet treat made from cocoa",
            'TITANIC': "Movie about a famous ship disaster",
            'BASKETBALL': "Sport played with hoops and a orange ball",
        }
    
    def get_word_hint(self):
        if self.word in self.word_hints:
            return f"💡 Word hint: {self.word_hints[self.word]}"
        return self.show_category_hint()
    
    def display_game_state(self):
        super().display_game_state()
        print("Extra commands: 'wordhint' for definition hint")
    
    def play_round(self):
        while not self.game_won and not self.game_lost:
            self.display_game_state()
            
            user_input = input("Your move: ").strip().lower()
            
            if user_input == 'quit':
                return False
            elif user_input == 'hint':
                print(self.get_hint())
                input("\nPress Enter to continue...")
                continue
            elif user_input == 'category':
                print(self.show_category_hint())
                input("\nPress Enter to continue...")
                continue
            elif user_input == 'wordhint':
                print(self.get_word_hint())
                input("\nPress Enter to continue...")
                continue
            elif len(user_input) == 1 and user_input.isalpha():
                letter = user_input.upper()
                if letter not in self.guessed_letters:
                    self.make_guess(letter)
                else:
                    print(f"You already guessed '{letter}'. Try a different letter.")
                    input("\nPress Enter to continue...")
            else:
                print("Please enter a single letter, 'hint', 'category', 'wordhint', or 'quit'.")
                input("\nPress Enter to continue...")
        
        # Game over
        self.display_game_state()
        
        if self.game_won:
            score = max(100 - (self.wrong_guesses * 10), 10)
            print(f"🎉 Congratulations! You won!")
            print(f"The word was: {self.word}")
            print(f"You made {self.wrong_guesses} wrong guesses.")
            print(f"Your score: {score} points")
        else:
            print(f"😵 Game Over! You lost!")
            print(f"The word was: {self.word}")
        
        return True

def main():
    while True:
        print("\n" + "="*40)
        print("🎯 HANGMAN GAME 🎯")
        print("="*40)
        print("1. Classic Hangman")
        print("2. Enhanced Hangman (with word hints)")
        print("3. Quit")
        
        choice = input("\nChoose game mode (1-3): ").strip()
        
        if choice == '1':
            game = HangmanGame()
            game.play()
        elif choice == '2':
            game = WordHintGame()
            game.play()
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

