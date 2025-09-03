import random
import sys
from collections import defaultdict

class RockPaperScissors:
    def __init__(self):
        self.classic_moves = {
            'rock': {'beats': ['scissors'], 'emoji': '🪨'},
            'paper': {'beats': ['rock'], 'emoji': '📄'},
            'scissors': {'beats': ['paper'], 'emoji': '✂️'}
        }
        
        self.extended_moves = {
            'rock': {'beats': ['scissors', 'lizard'], 'emoji': '🪨'},
            'paper': {'beats': ['rock', 'spock'], 'emoji': '📄'},
            'scissors': {'beats': ['paper', 'lizard'], 'emoji': '✂️'},
            'lizard': {'beats': ['spock', 'paper'], 'emoji': '🦎'},
            'spock': {'beats': ['scissors', 'rock'], 'emoji': '🖖'}
        }
        
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round_number = 0
        self.game_history = []
        self.player_move_frequency = defaultdict(int)
        self.computer_strategy = 'random'
        
    def get_valid_moves(self, extended=False):
        return self.extended_moves if extended else self.classic_moves
    
    def display_moves(self, moves):
        print("\nAvailable moves:")
        for move, data in moves.items():
            beats = ", ".join(data['beats'])
            print(f"  {data['emoji']} {move.title()} - beats {beats}")
    
    def get_player_move(self, moves):
        valid_moves = list(moves.keys())
        
        while True:
            move = input(f"\nYour move ({'/'.join(valid_moves)} or 'q' to quit): ").strip().lower()
            
            if move == 'q':
                return None
            elif move in valid_moves:
                return move
            else:
                print(f"Invalid move! Choose from: {', '.join(valid_moves)}")
    
    def get_computer_move(self, moves, player_history=None):
        valid_moves = list(moves.keys())
        
        if self.computer_strategy == 'random' or not player_history:
            return random.choice(valid_moves)
        elif self.computer_strategy == 'counter':
            # Try to counter the player's most frequent move
            if player_history:
                most_frequent = max(self.player_move_frequency, key=self.player_move_frequency.get)
                # Find a move that beats the player's favorite
                for move, data in moves.items():
                    if most_frequent in data['beats']:
                        return move
            return random.choice(valid_moves)
        elif self.computer_strategy == 'adaptive':
            # Mix of random and counter-strategy
            if random.random() < 0.7 and len(player_history) > 2:
                # Look at last 3 moves and try to predict
                recent_moves = player_history[-3:]
                most_recent = max(set(recent_moves), key=recent_moves.count)
                for move, data in moves.items():
                    if most_recent in data['beats']:
                        return move
            return random.choice(valid_moves)
    
    def determine_winner(self, player_move, computer_move, moves):
        if player_move == computer_move:
            return 'tie'
        elif computer_move in moves[player_move]['beats']:
            return 'player'
        else:
            return 'computer'
    
    def update_scores(self, result):
        if result == 'player':
            self.player_score += 1
        elif result == 'computer':
            self.computer_score += 1
        else:
            self.ties += 1
    
    def display_round_result(self, player_move, computer_move, result, moves):
        print(f"\n--- Round {self.round_number} ---")
        print(f"You: {moves[player_move]['emoji']} {player_move.title()}")
        print(f"Computer: {moves[computer_move]['emoji']} {computer_move.title()}")
        
        if result == 'tie':
            print("🤝 It's a tie!")
        elif result == 'player':
            print(f"🎉 You win! {player_move.title()} beats {computer_move}")
        else:
            print(f"🤖 Computer wins! {computer_move.title()} beats {player_move}")
    
    def display_scores(self):
        total_games = self.player_score + self.computer_score + self.ties
        if total_games > 0:
            win_rate = (self.player_score / total_games) * 100
            print(f"\n📈 Score: You {self.player_score} - {self.computer_score} Computer (Ties: {self.ties})")
            print(f"Your win rate: {win_rate:.1f}%")
    
    def show_statistics(self):
        if not self.game_history:
            return
        
        print("\n📉 Game Statistics:")
        print(f"Total rounds: {len(self.game_history)}")
        
        # Most used moves
        if self.player_move_frequency:
            most_used = max(self.player_move_frequency, key=self.player_move_frequency.get)
            print(f"Your favorite move: {most_used.title()} ({self.player_move_frequency[most_used]} times)")
        
        # Longest winning/losing streaks
        current_streak = 0
        max_win_streak = 0
        max_lose_streak = 0
        current_type = None
        
        for result in [game[2] for game in self.game_history]:
            if result == 'player':
                if current_type == 'player':
                    current_streak += 1
                else:
                    current_streak = 1
                    current_type = 'player'
                max_win_streak = max(max_win_streak, current_streak)
            elif result == 'computer':
                if current_type == 'computer':
                    current_streak += 1
                else:
                    current_streak = 1
                    current_type = 'computer'
                max_lose_streak = max(max_lose_streak, current_streak)
            else:
                current_streak = 0
                current_type = None
        
        if max_win_streak > 0:
            print(f"Longest winning streak: {max_win_streak}")
        if max_lose_streak > 0:
            print(f"Longest losing streak: {max_lose_streak}")
    
    def set_computer_difficulty(self):
        print("\n=== Computer Difficulty ===")
        print("1. Easy (Random moves)")
        print("2. Medium (Tries to counter your patterns)")
        print("3. Hard (Adaptive strategy)")
        
        while True:
            choice = input("\nSelect difficulty (1-3): ").strip()
            if choice == '1':
                self.computer_strategy = 'random'
                print("Computer will play randomly.")
                break
            elif choice == '2':
                self.computer_strategy = 'counter'
                print("Computer will try to counter your most used moves.")
                break
            elif choice == '3':
                self.computer_strategy = 'adaptive'
                print("Computer will use adaptive strategy.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def play_classic(self):
        print("🪨 📄 ✂️ Classic Rock Paper Scissors!")
        self.set_computer_difficulty()
        moves = self.get_valid_moves(extended=False)
        self.display_moves(moves)
        
        while True:
            self.round_number += 1
            player_move = self.get_player_move(moves)
            
            if player_move is None:
                break
            
            self.player_move_frequency[player_move] += 1
            computer_move = self.get_computer_move(moves, [game[0] for game in self.game_history])
            
            result = self.determine_winner(player_move, computer_move, moves)
            self.update_scores(result)
            self.game_history.append((player_move, computer_move, result))
            
            self.display_round_result(player_move, computer_move, result, moves)
            self.display_scores()
    
    def play_extended(self):
        print("🪨 📄 ✂️ 🦎 🖖 Rock Paper Scissors Lizard Spock!")
        print("(Based on The Big Bang Theory)")
        self.set_computer_difficulty()
        moves = self.get_valid_moves(extended=True)
        self.display_moves(moves)
        
        while True:
            self.round_number += 1
            player_move = self.get_player_move(moves)
            
            if player_move is None:
                break
            
            self.player_move_frequency[player_move] += 1
            computer_move = self.get_computer_move(moves, [game[0] for game in self.game_history])
            
            result = self.determine_winner(player_move, computer_move, moves)
            self.update_scores(result)
            self.game_history.append((player_move, computer_move, result))
            
            self.display_round_result(player_move, computer_move, result, moves)
            self.display_scores()

class TournamentMode(RockPaperScissors):
    def __init__(self):
        super().__init__()
        self.target_wins = 5
    
    def set_target_wins(self):
        while True:
            try:
                target = int(input("First to how many wins? (3-10): "))
                if 3 <= target <= 10:
                    self.target_wins = target
                    break
                else:
                    print("Please enter between 3 and 10.")
            except ValueError:
                print("Please enter a valid number.")
    
    def play_tournament(self, extended=False):
        print(f"\n🏆 Tournament Mode - First to {self.target_wins} wins!")
        
        moves = self.get_valid_moves(extended=extended)
        self.display_moves(moves)
        
        while self.player_score < self.target_wins and self.computer_score < self.target_wins:
            self.round_number += 1
            player_move = self.get_player_move(moves)
            
            if player_move is None:
                print("Tournament cancelled.")
                return
            
            computer_move = self.get_computer_move(moves)
            result = self.determine_winner(player_move, computer_move, moves)
            self.update_scores(result)
            
            self.display_round_result(player_move, computer_move, result, moves)
            self.display_scores()
            
            # Check for winner
            if self.player_score == self.target_wins:
                print(f"\n🏆 TOURNAMENT WINNER: YOU! 🏆")
                print(f"You won {self.target_wins}-{self.computer_score}!")
                break
            elif self.computer_score == self.target_wins:
                print(f"\n🤖 TOURNAMENT WINNER: COMPUTER! 🤖")
                print(f"Computer won {self.target_wins}-{self.player_score}!")
                break

def main():
    while True:
        print("\n" + "="*40)
        print("🪨 📄 ✂️ ROCK PAPER SCISSORS ✂️ 📄 🪨")
        print("="*40)
        print("1. Classic (Rock, Paper, Scissors)")
        print("2. Extended (+ Lizard, Spock)")
        print("3. Tournament Mode (Classic)")
        print("4. Tournament Mode (Extended)")
        print("5. Quit")
        
        choice = input("\nChoose game mode (1-5): ").strip()
        
        if choice == '1':
            game = RockPaperScissors()
            game.play_classic()
            game.show_statistics()
        elif choice == '2':
            game = RockPaperScissors()
            game.play_extended()
            game.show_statistics()
        elif choice == '3':
            game = TournamentMode()
            game.set_target_wins()
            game.play_tournament(extended=False)
            game.show_statistics()
        elif choice == '4':
            game = TournamentMode()
            game.set_target_wins()
            game.play_tournament(extended=True)
            game.show_statistics()
        elif choice == '5':
            print("Thanks for playing! 👋")
            break
        else:
            print("Invalid choice. Please try again.")
        
        if choice in ['1', '2', '3', '4']:
            play_again = input("\nPlay another game? (y/n): ").strip().lower()
            if play_again not in ['y', 'yes']:
                print("Thanks for playing! 👋")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye! 👋")
        sys.exit()

