# 🎮 Ultimate Python Game Collection

A comprehensive collection of classic games implemented in Python! From arcade classics to brain-teasing puzzles, this collection has something for everyone.

## 🌟 Features

- **9 Complete Games** across multiple categories
- **Beautiful Terminal UI** with emojis and colors
- **Multiple Difficulty Levels** for most games
- **AI Opponents** in strategy games
- **Statistics Tracking** and scoring systems
- **Cross-Platform** - works on Windows, macOS, and Linux
- **Easy Installation** with automatic dependency management

## 🎯 Game Collection

### 🕹️ Arcade Games
1. **Snake Game** - Classic snake with pygame graphics
2. **Pong** - The original paddle ball game
3. **Tetris** - Falling blocks puzzle classic
4. **Breakout** - Brick-breaking arcade action

### 🧠 Strategy Games
5. **Tic-Tac-Toe** - Play vs human or intelligent AI using minimax algorithm

### 🧩 Puzzle Games
6. **Number Guessing Game** - Guess the number with hints and multiple difficulty levels
7. **Memory Match** - Card matching with time attack mode

### 📝 Word Games
8. **Hangman** - Word guessing with categories and hints

### 🎲 Classic Games
9. **Rock Paper Scissors** - Classic + extended Lizard Spock mode

## 🚀 Quick Start

### Method 1: Game Launcher (Recommended)
```bash
python game_launcher.py
```
The launcher provides:
- Easy game selection by category
- Automatic dependency checking
- One-click installation of requirements
- Help and instructions

### Method 2: Direct Game Launch
```bash
# For games without dependencies
python tictactoe_game.py
python hangman_game.py
python number_guessing_game.py
python rock_paper_scissors.py
python memory_match_game.py
python breakout_game.py

# For pygame games (requires pygame)
python snake_game.py
python pong_game.py
python tetris_game.py
```

## 📋 Requirements

### System Requirements
- Python 3.6 or higher
- Windows, macOS, or Linux

### Game Dependencies
- **No dependencies**: Tic-Tac-Toe, Hangman, Number Guessing, Rock Paper Scissors, Memory Match, Breakout
- **Pygame required**: Snake, Pong, Tetris

### Installing Dependencies
```bash
# Automatic installation via launcher
python game_launcher.py
# Then select option 'i' to install missing requirements

# Manual installation
pip install pygame
```

## 🎮 Game Details

### Snake Game 🐍
- **Type**: Arcade
- **Features**: Smooth pygame graphics, score tracking, collision detection
- **Controls**: Arrow keys to move
- **Goal**: Eat food to grow while avoiding walls and yourself

### Tic-Tac-Toe ⭕
- **Type**: Strategy
- **Features**: Human vs Human, Human vs AI (minimax algorithm)
- **Controls**: Enter coordinates (e.g., "1,2")
- **Goal**: Get three in a row

### Number Guessing Game 🔢
- **Type**: Puzzle
- **Features**: Multiple difficulties, hints, statistics, multiplayer
- **Controls**: Type numbers and commands
- **Goal**: Guess the secret number in minimum attempts

### Rock Paper Scissors 🪨📄✂️
- **Type**: Classic
- **Features**: Classic mode, Extended mode (Lizard Spock), Tournament mode
- **Controls**: Type your choice
- **Goal**: Beat the computer in best of matches

### Hangman 🎯
- **Type**: Word
- **Features**: 6 categories, hints, difficulty levels, scoring
- **Controls**: Type letters
- **Goal**: Guess the word before the drawing is complete

### Memory Match 🧠
- **Type**: Memory
- **Features**: Multiple grid sizes, time attack mode, scoring
- **Controls**: Enter coordinates of cards
- **Goal**: Match all pairs of cards

### Breakout 🧱
- **Type**: Arcade
- **Features**: Turn-based and real-time modes, multiple levels
- **Controls**: 'a'/'d' to move paddle
- **Goal**: Break all bricks with your ball

### Pong 🏓
- **Type**: Arcade
- **Features**: Classic paddle gameplay with pygame
- **Controls**: Up/Down arrow keys
- **Goal**: Score points by getting ball past opponent

### Tetris 🧱
- **Type**: Puzzle
- **Features**: Classic falling blocks with pygame graphics
- **Controls**: Arrow keys to move/rotate pieces
- **Goal**: Clear lines by filling rows completely

## 🎯 Game Features

### Difficulty Levels
- **Easy**: Beginner-friendly settings
- **Medium**: Balanced challenge
- **Hard**: For experienced players
- **Expert**: Ultimate challenge
- **Custom**: Create your own difficulty

### AI Intelligence
- **Tic-Tac-Toe**: Minimax algorithm (unbeatable)
- **Rock Paper Scissors**: Adaptive strategy that learns your patterns

### Statistics Tracking
- Games played and won
- Win rates and averages
- High scores
- Performance metrics

## 🛠️ Development

### File Structure
```
games/
├── game_launcher.py          # Main launcher application
├── snake_game.py             # Snake game implementation
├── tictactoe_game.py         # Tic-tac-toe with AI
├── number_guessing_game.py   # Number guessing with features
├── rock_paper_scissors.py    # RPS with extensions
├── hangman_game.py           # Hangman with categories
├── memory_match_game.py      # Memory matching game
├── breakout_game.py          # Breakout arcade game
├── pong_game.py              # Classic pong (existing)
├── tetris_game.py            # Tetris puzzle (existing)
├── *.yaml                    # Game configuration files
└── README.md                 # This file
```

### Technical Implementation
- **Object-oriented design** with clean class structures
- **Error handling** for robust gameplay
- **Cross-platform compatibility** using standard libraries
- **Modular architecture** - each game is self-contained
- **Configuration files** for easy game management

## 🎊 Getting Started

1. **Clone or download** this game collection
2. **Navigate** to the games directory
3. **Run the launcher**: `python game_launcher.py`
4. **Install dependencies** if prompted (option 'i')
5. **Choose a game** and start playing!

## 🤝 Contributing

Want to add more games or improve existing ones? Here's how:

1. Follow the existing code structure
2. Add appropriate error handling
3. Include difficulty levels where applicable
4. Add statistics tracking
5. Create a corresponding YAML configuration file
6. Update the game launcher

## 📝 License

This game collection is open source and available for educational and personal use.

## 🎮 Have Fun!

Enjoy this collection of classic games! Whether you're looking for a quick brain teaser or an extended gaming session, there's something here for everyone.

**Happy Gaming!** 🎯🎲🕹️

