"""
High score persistence system
"""
import json
import os

HIGH_SCORE_FILE = "high_score.json"

def load_high_score(game_name="snake"):
    """Load the high score from file for a specific game, return 0 if file doesn't exist"""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get(game_name, {}).get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            return 0
    return 0

def save_high_score(score, game_name="snake"):
    """Save the high score to file for a specific game"""
    try:
        data = {}
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = {}
        
        if game_name not in data:
            data[game_name] = {}
        data[game_name]['high_score'] = score
        
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass  # Silently fail if we can't write

def update_high_score(score, game_name="snake"):
    """Update high score if the new score is higher for a specific game"""
    current_high = load_high_score(game_name)
    if score > current_high:
        save_high_score(score, game_name)
        return True
    return False

