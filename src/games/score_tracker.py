#!/usr/bin/env python3
"""
Score Tracker Helper
Simple interface for games to record scores and statistics
"""

import time
from scoreboard import GameScoreboard

class ScoreTracker:
    def __init__(self):
        self.scoreboard = GameScoreboard()
        self.session_start = None
        self.current_user = None
        self.current_game = None
    
    def start_session(self, username, game_id):
        """Start a new game session"""
        self.current_user = username
        self.current_game = game_id
        self.session_start = time.time()
        print(f"\n🎮 Welcome {username}! Starting {game_id} session...")
    
    def end_session(self, score, won=False, details=None):
        """End the current session and record the score"""
        if not self.current_user or not self.current_game:
            return
        
        duration = int(time.time() - self.session_start) if self.session_start else 0
        
        session_data = {
            'score': score,
            'duration': duration,
            'won': won,
            'details': details or {}
        }
        
        # Record the session
        self.scoreboard.record_game_session(
            self.current_user, 
            self.current_game, 
            session_data
        )
        
        print(f"\n📊 Session recorded: {score} points in {duration}s")
        
        # Reset session
        self.current_user = None
        self.current_game = None
        self.session_start = None
    
    def get_user_input(self, prompt="Enter your username: "):
        """Get username from user"""
        username = input(prompt).strip()
        if not username:
            username = "Guest"
        return username
    
    def show_quick_stats(self, username, game_id):
        """Show quick stats for the user in this game"""
        stats = self.scoreboard.get_user_stats(username)
        if stats and game_id in stats['game_stats']:
            game_stats = stats['game_stats'][game_id]
            print(f"\n📈 Your {game_stats['name']} Stats:")
            print(f"   Games Played: {game_stats['games_played']}")
            print(f"   High Score: {game_stats['high_score']:,}")
            print(f"   Average: {game_stats['average_score']:.1f}")

# Easy-to-use functions for games
def start_game_session(username, game_id):
    """Start tracking a game session"""
    tracker = ScoreTracker()
    tracker.start_session(username, game_id)
    return tracker

def record_score(username, game_id, score, won=False, duration=0, details=None):
    """Quick function to record a score"""
    scoreboard = GameScoreboard()
    session_data = {
        'score': score,
        'duration': duration,
        'won': won,
        'details': details or {}
    }
    scoreboard.record_game_session(username, game_id, session_data)
    print(f"\n📊 Score recorded: {username} scored {score} in {game_id}")

def get_username():
    """Simple username input"""
    username = input("\n🎮 Enter your username (or press Enter for Guest): ").strip()
    return username if username else "Guest"

def show_leaderboard(game_id):
    """Quick leaderboard display"""
    scoreboard = GameScoreboard()
    scoreboard.display_leaderboard(game_id, limit=5)

