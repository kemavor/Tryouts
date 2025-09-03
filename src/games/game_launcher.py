#!/usr/bin/env python3
"""
Game Collection Launcher
A comprehensive collection of classic games implemented in Python
"""

import os
import sys
import subprocess
from pathlib import Path

class GameLauncher:
    def __init__(self):
        self.games_dir = Path(__file__).parent
        self.games = {
            '1': {
                'name': 'Snake Game',
                'file': 'snake_game.py',
                'description': 'Classic Snake game with pygame graphics',
                'category': 'Arcade',
                'requires': ['pygame']
            },
            '2': {
                'name': 'Tic-Tac-Toe',
                'file': 'tictactoe_game.py',
                'description': 'Play vs human or intelligent AI',
                'category': 'Strategy',
                'requires': []
            },
            '3': {
                'name': 'Number Guessing Game',
                'file': 'number_guessing_game.py',
                'description': 'Guess the number with hints and statistics',
                'category': 'Puzzle',
                'requires': []
            },
            '4': {
                'name': 'Rock Paper Scissors',
                'file': 'rock_paper_scissors.py',
                'description': 'Classic + extended Lizard Spock mode',
                'category': 'Classic',
                'requires': []
            },
            '5': {
                'name': 'Hangman',
                'file': 'hangman_game.py',
                'description': 'Word guessing with categories and hints',
                'category': 'Word',
                'requires': []
            },
            '6': {
                'name': 'Memory Match',
                'file': 'memory_match_game.py',
                'description': 'Card matching with time attack mode',
                'category': 'Memory',
                'requires': []
            },
            '7': {
                'name': 'Breakout',
                'file': 'breakout_game.py',
                'description': 'Brick-breaking arcade game',
                'category': 'Arcade',
                'requires': []
            },
            '8': {
                'name': 'Pong',
                'file': 'pong_game.py',
                'description': 'Classic paddle ball game',
                'category': 'Arcade',
                'requires': ['pygame']
            },
            '9': {
                'name': 'Tetris',
                'file': 'tetris_game.py',
                'description': 'Classic falling blocks puzzle',
                'category': 'Puzzle',
                'requires': ['pygame']
            }
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def check_requirements(self, game_id):
        """Check if required modules are available"""
        game = self.games[game_id]
        missing = []
        
        for module in game['requires']:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        return missing
    
    def install_requirements(self, modules):
        """Attempt to install missing modules"""
        print(f"\n💾 Installing required modules: {', '.join(modules)}")
        
        for module in modules:
            try:
                print(f"Installing {module}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
                print(f"✅ {module} installed successfully!")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {module}")
                return False
        
        return True
    
    def show_main_menu(self):
        self.clear_screen()
        print("" + "="*60)
        print("🎮     WELCOME TO THE ULTIMATE GAME COLLECTION!     🎮")
        print("="*60)
        print()
        print("Choose your game:")
        print()
        
        # Group games by category
        categories = {}
        for game_id, game in self.games.items():
            category = game['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((game_id, game))
        
        # Display games by category
        for category, games in categories.items():
            print(f"🏷️  {category} Games:")
            for game_id, game in games:
                status = ""
                missing = self.check_requirements(game_id)
                if missing:
                    status = f" 💾 (requires: {', '.join(missing)})"
                
                print(f"   {game_id}. {game['name']}{status}")
                print(f"      {game['description']}")
            print()
        
        print("🔧 Utilities:")
        print("   i. Install missing requirements")
        print("   l. List all available games")
        print("   s. View Scoreboard")
        print("   h. Help & Instructions")
        print("   q. Quit")
        print()
    
    def show_game_list(self):
        self.clear_screen()
        print("📋 COMPLETE GAME LIST")
        print("="*50)
        
        for game_id, game in self.games.items():
            missing = self.check_requirements(game_id)
            status = "✅ Ready" if not missing else f"❌ Missing: {', '.join(missing)}"
            
            print(f"{game_id}. {game['name']}")
            print(f"   Category: {game['category']}")
            print(f"   File: {game['file']}")
            print(f"   Status: {status}")
            print(f"   Description: {game['description']}")
            print()
        
        input("Press Enter to continue...")
    
    def show_help(self):
        self.clear_screen()
        print("📚 HELP & INSTRUCTIONS")
        print("="*50)
        print()
        print("🎮 Game Collection Features:")
        print("• 9 different games across multiple categories")
        print("• Arcade games: Snake, Pong, Tetris, Breakout")
        print("• Strategy games: Tic-Tac-Toe with AI")
        print("• Puzzle games: Number Guessing, Memory Match")
        print("• Word games: Hangman with categories")
        print("• Classic games: Rock Paper Scissors")
        print()
        print("🔧 Technical Requirements:")
        print("• Python 3.6+ required")
        print("• Some games require pygame (will auto-install)")
        print("• All games work on Windows, macOS, and Linux")
        print()
        print("🎲 How to Play:")
        print("1. Select a game number from the main menu")
        print("2. If requirements are missing, choose 'i' to install")
        print("3. Follow the in-game instructions")
        print("4. Press Ctrl+C to quit any game anytime")
        print()
        print("💾 Installation:")
        print("• Use option 'i' to install missing requirements")
        print("• Games without requirements work immediately")
        print("• Pygame games have better graphics but need installation")
        print()
        print("🏆 Game Features:")
        print("• Multiple difficulty levels")
        print("• Score tracking and statistics")
        print("• AI opponents in some games")
        print("• Both single and multiplayer modes")
        print("• Colorful emoji-based interfaces")
        print()
        
        input("Press Enter to continue...")
    
    def install_missing_requirements(self):
        self.clear_screen()
        print("💾 INSTALL REQUIREMENTS")
        print("="*40)
        
        all_missing = set()
        games_needing_install = []
        
        for game_id, game in self.games.items():
            missing = self.check_requirements(game_id)
            if missing:
                all_missing.update(missing)
                games_needing_install.append(f"{game['name']} (needs: {', '.join(missing)})")
        
        if not all_missing:
            print("✅ All requirements are already installed!")
            print("All games are ready to play.")
            input("\nPress Enter to continue...")
            return
        
        print("Games needing installation:")
        for game in games_needing_install:
            print(f"  • {game}")
        print()
        print(f"Modules to install: {', '.join(all_missing)}")
        print()
        
        choice = input("Install all missing requirements? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            success = self.install_requirements(list(all_missing))
            if success:
                print("\n✅ All requirements installed successfully!")
                print("You can now play all games.")
            else:
                print("\n❌ Some installations failed.")
                print("You can still play games that don't require those modules.")
        
        input("\nPress Enter to continue...")
    
    def launch_game(self, game_id):
        if game_id not in self.games:
            print("Invalid game selection!")
            return
        
        game = self.games[game_id]
        missing = self.check_requirements(game_id)
        
        if missing:
            print(f"\n❌ Cannot launch {game['name']}")
            print(f"Missing requirements: {', '.join(missing)}")
            print("Use option 'i' to install requirements.")
            input("\nPress Enter to continue...")
            return
        
        game_file = self.games_dir / game['file']
        if not game_file.exists():
            print(f"\n❌ Game file not found: {game['file']}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n🚀 Launching {game['name']}...")
        print("Press Ctrl+C to return to the main menu anytime.")
        print("="*50)
        
        try:
            # Change to games directory and run the game
            original_dir = os.getcwd()
            os.chdir(self.games_dir)
            
            subprocess.run([sys.executable, game['file']])
            
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
        except Exception as e:
            print(f"\n❌ Error launching game: {e}")
        finally:
            os.chdir(original_dir)
            input("\nPress Enter to continue...")
    
    def run(self):
        """Main launcher loop"""
        print("🎮 Welcome to the Game Collection! 🎮")
        print("Loading...")
        
        while True:
            try:
                self.show_main_menu()
                
                choice = input("Your choice: ").strip().lower()
                
                if choice == 'q':
                    print("\nThanks for playing! 👋")
                    print("Come back anytime for more gaming fun!")
                    break
                elif choice == 'i':
                    self.install_missing_requirements()
                elif choice == 'l':
                    self.show_game_list()
                elif choice == 's':
                    self.show_scoreboard()
                elif choice == 'h':
                    self.show_help()
                elif choice in self.games:
                    self.launch_game(choice)
                else:
                    print("\n❌ Invalid choice. Please try again.")
                    input("Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\nThanks for playing! 👋")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")

def main():
    """Entry point for the game launcher"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

