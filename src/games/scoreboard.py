#!/usr/bin/env python3
"""
Universal Scoreboard System
Tracks user performance across all games in the collection
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import statistics

class GameScoreboard:
    def __init__(self):
        self.data_file = Path(__file__).parent / "scoreboard_data.json"
        self.data = self.load_data()
        
        # Game configurations
        self.game_configs = {
            'snake': {
                'name': '🐍 Snake',
                'score_type': 'points',
                'higher_better': True,
                'stats': ['high_score', 'games_played', 'average_score']
            },
            'tictactoe': {
                'name': '⭕ Tic-Tac-Toe',
                'score_type': 'wins',
                'higher_better': True,
                'stats': ['wins', 'losses', 'ties', 'win_rate']
            },
            'number_guessing': {
                'name': '🔢 Number Guessing',
                'score_type': 'score',
                'higher_better': True,
                'stats': ['high_score', 'games_won', 'average_attempts', 'win_rate']
            },
            'rock_paper_scissors': {
                'name': '🪨📄✂️ Rock Paper Scissors',
                'score_type': 'wins',
                'higher_better': True,
                'stats': ['wins', 'losses', 'ties', 'win_rate', 'streak']
            },
            'hangman': {
                'name': '🎯 Hangman',
                'score_type': 'score',
                'higher_better': True,
                'stats': ['high_score', 'words_guessed', 'win_rate', 'average_wrong_guesses']
            },
            'memory_match': {
                'name': '🧠 Memory Match',
                'score_type': 'score',
                'higher_better': True,
                'stats': ['high_score', 'best_time', 'perfect_games', 'average_attempts']
            },
            'breakout': {
                'name': '🎮 Breakout',
                'score_type': 'score',
                'higher_better': True,
                'stats': ['high_score', 'levels_completed', 'total_bricks_broken']
            },
            'pong': {
                'name': '🏓 Pong',
                'score_type': 'points',
                'higher_better': True,
                'stats': ['high_score', 'games_won', 'win_rate']
            },
            'tetris': {
                'name': '🧱 Tetris',
                'score_type': 'points',
                'higher_better': True,
                'stats': ['high_score', 'lines_cleared', 'level_reached']
            }
        }
    
    def load_data(self):
        """Load scoreboard data from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return self.create_empty_data()
        return self.create_empty_data()
    
    def create_empty_data(self):
        """Create empty scoreboard data structure"""
        return {
            'users': {},
            'global_stats': {},
            'achievements': {},
            'last_updated': datetime.now().isoformat()
        }
    
    def save_data(self):
        """Save scoreboard data to JSON file"""
        self.data['last_updated'] = datetime.now().isoformat()
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving scoreboard data: {e}")
            return False
    
    def get_or_create_user(self, username):
        """Get user data or create new user"""
        if username not in self.data['users']:
            self.data['users'][username] = {
                'created': datetime.now().isoformat(),
                'last_played': datetime.now().isoformat(),
                'total_playtime': 0,
                'games': {},
                'achievements': [],
                'favorite_game': None,
                'total_score': 0
            }
            
            # Initialize game stats for each game
            for game_id in self.game_configs:
                self.data['users'][username]['games'][game_id] = {
                    'games_played': 0,
                    'total_score': 0,
                    'high_score': 0,
                    'sessions': []
                }
        
        return self.data['users'][username]
    
    def record_game_session(self, username, game_id, session_data):
        """Record a game session for a user"""
        user = self.get_or_create_user(username)
        
        if game_id not in user['games']:
            user['games'][game_id] = {
                'games_played': 0,
                'total_score': 0,
                'high_score': 0,
                'sessions': []
            }
        
        # Update user's last played time
        user['last_played'] = datetime.now().isoformat()
        
        # Record the session
        session = {
            'timestamp': datetime.now().isoformat(),
            'score': session_data.get('score', 0),
            'duration': session_data.get('duration', 0),
            'won': session_data.get('won', False),
            'details': session_data.get('details', {})
        }
        
        user['games'][game_id]['sessions'].append(session)
        user['games'][game_id]['games_played'] += 1
        user['games'][game_id]['total_score'] += session['score']
        
        # Update high score
        if session['score'] > user['games'][game_id]['high_score']:
            user['games'][game_id]['high_score'] = session['score']
        
        # Update user's total score
        user['total_score'] += session['score']
        
        # Update playtime
        user['total_playtime'] += session['duration']
        
        # Check for achievements
        self.check_achievements(username, game_id, session)
        
        # Save data
        self.save_data()
        
        return session
    
    def check_achievements(self, username, game_id, session):
        """Check and award achievements"""
        user = self.data['users'][username]
        game_stats = user['games'][game_id]
        
        achievements = [
            # First game achievements
            {
                'id': f'first_{game_id}',
                'name': f'First {self.game_configs[game_id]["name"]} Game',
                'description': f'Played your first game of {self.game_configs[game_id]["name"]}',
                'condition': lambda: game_stats['games_played'] == 1
            },
            
            # Milestone achievements
            {
                'id': f'{game_id}_veteran',
                'name': f'{self.game_configs[game_id]["name"]} Veteran',
                'description': f'Played 10 games of {self.game_configs[game_id]["name"]}',
                'condition': lambda: game_stats['games_played'] >= 10
            },
            
            # High score achievements
            {
                'id': f'{game_id}_high_scorer',
                'name': f'{self.game_configs[game_id]["name"]} High Scorer',
                'description': f'Achieved a score of 1000+ in {self.game_configs[game_id]["name"]}',
                'condition': lambda: session['score'] >= 1000
            },
            
            # Global achievements
            {
                'id': 'game_explorer',
                'name': '🎮 Game Explorer',
                'description': 'Played at least 3 different games',
                'condition': lambda: len([g for g in user['games'] if user['games'][g]['games_played'] > 0]) >= 3
            },
            
            {
                'id': 'dedicated_player',
                'name': '🏆 Dedicated Player',
                'description': 'Played 50 games total across all games',
                'condition': lambda: sum(user['games'][g]['games_played'] for g in user['games']) >= 50
            },
            
            {
                'id': 'score_master',
                'name': '⭐ Score Master',
                'description': 'Achieved a total score of 10,000 across all games',
                'condition': lambda: user['total_score'] >= 10000
            }
        ]
        
        for achievement in achievements:
            if achievement['id'] not in user['achievements']:
                try:
                    if achievement['condition']():
                        user['achievements'].append(achievement['id'])
                        print(f"\n🏆 ACHIEVEMENT UNLOCKED: {achievement['name']}")
                        print(f"   {achievement['description']}")
                except:
                    pass  # Skip if condition check fails
    
    def get_user_stats(self, username):
        """Get comprehensive stats for a user"""
        if username not in self.data['users']:
            return None
        
        user = self.data['users'][username]
        stats = {
            'username': username,
            'total_score': user['total_score'],
            'total_games': sum(user['games'][g]['games_played'] for g in user['games']),
            'total_playtime': user['total_playtime'],
            'achievements_count': len(user['achievements']),
            'games_played': len([g for g in user['games'] if user['games'][g]['games_played'] > 0]),
            'favorite_game': self.get_favorite_game(username),
            'recent_activity': self.get_recent_activity(username),
            'game_stats': {}
        }
        
        # Calculate per-game stats
        for game_id, game_data in user['games'].items():
            if game_data['games_played'] > 0:
                stats['game_stats'][game_id] = {
                    'name': self.game_configs[game_id]['name'],
                    'games_played': game_data['games_played'],
                    'high_score': game_data['high_score'],
                    'average_score': game_data['total_score'] / game_data['games_played'],
                    'last_played': self.get_last_played_date(username, game_id)
                }
        
        return stats
    
    def get_favorite_game(self, username):
        """Determine user's favorite game based on play time"""
        user = self.data['users'][username]
        max_games = 0
        favorite = None
        
        for game_id, game_data in user['games'].items():
            if game_data['games_played'] > max_games:
                max_games = game_data['games_played']
                favorite = game_id
        
        return self.game_configs[favorite]['name'] if favorite else None
    
    def get_recent_activity(self, username, days=7):
        """Get recent activity for a user"""
        user = self.data['users'][username]
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = []
        
        for game_id, game_data in user['games'].items():
            for session in game_data['sessions']:
                session_date = datetime.fromisoformat(session['timestamp'])
                if session_date >= cutoff_date:
                    recent_sessions.append({
                        'game': self.game_configs[game_id]['name'],
                        'score': session['score'],
                        'date': session_date,
                        'won': session.get('won', False)
                    })
        
        return sorted(recent_sessions, key=lambda x: x['date'], reverse=True)
    
    def get_last_played_date(self, username, game_id):
        """Get the last played date for a specific game"""
        user = self.data['users'][username]
        sessions = user['games'][game_id]['sessions']
        
        if sessions:
            return sessions[-1]['timestamp']
        return None
    
    def get_leaderboard(self, game_id=None, limit=10):
        """Get leaderboard for a specific game or overall"""
        leaderboard = []
        
        for username, user_data in self.data['users'].items():
            if game_id:
                # Game-specific leaderboard
                if game_id in user_data['games'] and user_data['games'][game_id]['games_played'] > 0:
                    leaderboard.append({
                        'username': username,
                        'score': user_data['games'][game_id]['high_score'],
                        'games_played': user_data['games'][game_id]['games_played']
                    })
            else:
                # Overall leaderboard
                total_games = sum(user_data['games'][g]['games_played'] for g in user_data['games'])
                if total_games > 0:
                    leaderboard.append({
                        'username': username,
                        'score': user_data['total_score'],
                        'games_played': total_games,
                        'achievements': len(user_data['achievements'])
                    })
        
        # Sort by score (descending)
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        return leaderboard[:limit]
    
    def display_user_profile(self, username):
        """Display a user's complete profile"""
        stats = self.get_user_stats(username)
        if not stats:
            print(f"User '{username}' not found.")
            return
        
        print(f"\n{'='*60}")
        print(f"🎮 PLAYER PROFILE: {username.upper()}")
        print(f"{'='*60}")
        
        # Overview
        print(f"\n📊 OVERVIEW:")
        print(f"   Total Score: {stats['total_score']:,}")
        print(f"   Games Played: {stats['total_games']}")
        print(f"   Different Games: {stats['games_played']}/9")
        print(f"   Achievements: {stats['achievements_count']}")
        print(f"   Favorite Game: {stats['favorite_game'] or 'None yet'}")
        
        if stats['total_playtime'] > 0:
            hours = stats['total_playtime'] // 3600
            minutes = (stats['total_playtime'] % 3600) // 60
            print(f"   Total Playtime: {hours}h {minutes}m")
        
        # Game-specific stats
        if stats['game_stats']:
            print(f"\n🎯 GAME STATISTICS:")
            for game_id, game_stats in stats['game_stats'].items():
                print(f"\n   {game_stats['name']}:")
                print(f"      Games Played: {game_stats['games_played']}")
                print(f"      High Score: {game_stats['high_score']:,}")
                print(f"      Average Score: {game_stats['average_score']:.1f}")
        
        # Recent activity
        if stats['recent_activity']:
            print(f"\n📅 RECENT ACTIVITY (Last 7 days):")
            for activity in stats['recent_activity'][:5]:
                date_str = activity['date'].strftime('%m/%d %H:%M')
                status = "🏆" if activity['won'] else "🎮"
                print(f"   {status} {activity['game']} - Score: {activity['score']} ({date_str})")
        
        # Achievements
        user = self.data['users'][username]
        if user['achievements']:
            print(f"\n🏆 ACHIEVEMENTS ({len(user['achievements'])})")
            achievement_names = {
                'game_explorer': '🎮 Game Explorer',
                'dedicated_player': '🏆 Dedicated Player',
                'score_master': '⭐ Score Master'
            }
            
            for achievement_id in user['achievements']:
                if achievement_id in achievement_names:
                    print(f"   {achievement_names[achievement_id]}")
                else:
                    print(f"   🏅 {achievement_id.replace('_', ' ').title()}")
    
    def display_leaderboard(self, game_id=None, limit=10):
        """Display leaderboard"""
        if game_id and game_id in self.game_configs:
            game_name = self.game_configs[game_id]['name']
            print(f"\n🏆 {game_name.upper()} LEADERBOARD")
        else:
            print(f"\n🏆 OVERALL LEADERBOARD")
        
        print(f"{'='*50}")
        
        leaderboard = self.get_leaderboard(game_id, limit)
        
        if not leaderboard:
            print("   No scores recorded yet. Be the first to play!")
            return
        
        for i, entry in enumerate(leaderboard, 1):
            rank_emoji = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i:2d}."
            username = entry['username'][:15]  # Truncate long usernames
            score = entry['score']
            games = entry['games_played']
            
            if game_id:
                print(f"   {rank_emoji} {username:<15} {score:>8,} pts ({games} games)")
            else:
                achievements = entry.get('achievements', 0)
                print(f"   {rank_emoji} {username:<15} {score:>8,} pts ({games} games, {achievements} achievements)")
    
    def display_global_stats(self):
        """Display global statistics across all users"""
        print(f"\n📈 GLOBAL STATISTICS")
        print(f"{'='*40}")
        
        total_users = len(self.data['users'])
        total_games_played = 0
        total_score = 0
        most_popular_game = None
        game_popularity = defaultdict(int)
        
        for user_data in self.data['users'].values():
            total_score += user_data['total_score']
            for game_id, game_data in user_data['games'].items():
                games_played = game_data['games_played']
                total_games_played += games_played
                game_popularity[game_id] += games_played
        
        if game_popularity:
            most_popular_game_id = max(game_popularity, key=game_popularity.get)
            most_popular_game = self.game_configs[most_popular_game_id]['name']
        
        print(f"   Total Players: {total_users}")
        print(f"   Total Games Played: {total_games_played:,}")
        print(f"   Total Score Earned: {total_score:,}")
        print(f"   Most Popular Game: {most_popular_game or 'None yet'}")
        
        if total_users > 0:
            avg_score = total_score / total_users
            avg_games = total_games_played / total_users
            print(f"   Average Score per Player: {avg_score:.1f}")
            print(f"   Average Games per Player: {avg_games:.1f}")

def main():
    """Main scoreboard interface"""
    scoreboard = GameScoreboard()
    
    while True:
        print(f"\n{'='*50}")
        print(f"🏆 GAME COLLECTION SCOREBOARD")
        print(f"{'='*50}")
        print("1. View User Profile")
        print("2. View Overall Leaderboard")
        print("3. View Game-Specific Leaderboard")
        print("4. Global Statistics")
        print("5. Quit")
        
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            username = input("Enter username: ").strip()
            if username:
                scoreboard.display_user_profile(username)
            else:
                print("Please enter a valid username.")
        
        elif choice == '2':
            scoreboard.display_leaderboard()
        
        elif choice == '3':
            print("\nAvailable games:")
            for i, (game_id, config) in enumerate(scoreboard.game_configs.items(), 1):
                print(f"   {i}. {config['name']}")
            
            try:
                game_choice = int(input("\nSelect game number: ")) - 1
                game_ids = list(scoreboard.game_configs.keys())
                if 0 <= game_choice < len(game_ids):
                    scoreboard.display_leaderboard(game_ids[game_choice])
                else:
                    print("Invalid game selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '4':
            scoreboard.display_global_stats()
        
        elif choice == '5':
            print("Thanks for checking the scoreboard! 🏆")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye! 🏆")
        sys.exit(0)

