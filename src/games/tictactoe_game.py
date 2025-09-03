import os
import sys

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_board(self):
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  -----------")
        print()
    
    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)
    
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_move(self):
        while True:
            try:
                move = input(f"Player {self.current_player}, enter your move (row,col) or 'q' to quit: ").strip()
                if move.lower() == 'q':
                    return None, None
                
                if ',' in move:
                    row, col = map(int, move.split(','))
                else:
                    # Allow space-separated input too
                    row, col = map(int, move.split())
                
                if 0 <= row <= 2 and 0 <= col <= 2:
                    return row, col
                else:
                    print("Please enter coordinates between 0-2.")
            except (ValueError, IndexError):
                print("Please enter valid coordinates (e.g., '1,2' or '1 2').")
    
    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Enter coordinates as 'row,col' (e.g., '1,2')")
        print("Coordinates range from 0 to 2")
        print("Type 'q' to quit\n")
        
        while True:
            self.clear_screen()
            print("Welcome to Tic-Tac-Toe!")
            print("Enter coordinates as 'row,col' (e.g., '1,2')")
            print("Type 'q' to quit\n")
            
            self.display_board()
            
            row, col = self.get_move()
            if row is None:
                print("Thanks for playing!")
                break
            
            if self.make_move(row, col):
                winner = self.check_winner()
                if winner:
                    self.clear_screen()
                    print("Welcome to Tic-Tac-Toe!\n")
                    self.display_board()
                    print(f"🎉 Player {winner} wins!")
                    break
                elif self.is_board_full():
                    self.clear_screen()
                    print("Welcome to Tic-Tac-Toe!\n")
                    self.display_board()
                    print("It's a tie!")
                    break
                else:
                    self.switch_player()
            else:
                print("That position is already taken! Try again.")
                input("Press Enter to continue...")

class TicTacToeAI(TicTacToe):
    def __init__(self):
        super().__init__()
        self.human_player = 'X'
        self.ai_player = 'O'
    
    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        
        if winner == self.ai_player:
            return 1
        elif winner == self.human_player:
            return -1
        elif self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.ai_player
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.human_player
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.ai_player
                    score = self.minimax(0, False)
                    self.board[i][j] = ' '
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move
    
    def play_vs_ai(self):
        print("Welcome to Tic-Tac-Toe vs AI!")
        print("You are X, AI is O")
        print("Enter coordinates as 'row,col' (e.g., '1,2')")
        print("Type 'q' to quit\n")
        
        while True:
            self.clear_screen()
            print("Tic-Tac-Toe vs AI - You are X\n")
            self.display_board()
            
            if self.current_player == self.human_player:
                row, col = self.get_move()
                if row is None:
                    print("Thanks for playing!")
                    break
                
                if self.make_move(row, col):
                    winner = self.check_winner()
                    if winner:
                        self.clear_screen()
                        print("Tic-Tac-Toe vs AI\n")
                        self.display_board()
                        if winner == self.human_player:
                            print("🎉 You win!")
                        else:
                            print("🤖 AI wins!")
                        break
                    elif self.is_board_full():
                        self.clear_screen()
                        print("Tic-Tac-Toe vs AI\n")
                        self.display_board()
                        print("It's a tie!")
                        break
                    else:
                        self.switch_player()
                else:
                    print("That position is already taken! Try again.")
                    input("Press Enter to continue...")
            else:
                # AI's turn
                print("AI is thinking...")
                import time
                time.sleep(1)  # Add some drama
                
                row, col = self.get_best_move()
                self.make_move(row, col)
                
                winner = self.check_winner()
                if winner:
                    self.clear_screen()
                    print("Tic-Tac-Toe vs AI\n")
                    self.display_board()
                    if winner == self.human_player:
                        print("🎉 You win!")
                    else:
                        print("🤖 AI wins!")
                    break
                elif self.is_board_full():
                    self.clear_screen()
                    print("Tic-Tac-Toe vs AI\n")
                    self.display_board()
                    print("It's a tie!")
                    break
                else:
                    self.switch_player()

def main():
    while True:
        print("\n=== TIC-TAC-TOE ===\n")
        print("1. Play vs Human")
        print("2. Play vs AI")
        print("3. Quit")
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == '1':
            game = TicTacToe()
            game.play()
        elif choice == '2':
            game = TicTacToeAI()
            game.play_vs_ai()
        elif choice == '3':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        if choice in ['1', '2']:
            play_again = input("\nPlay again? (y/n): ").strip().lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye!")
        sys.exit()

