"""
High score persistence system
"""
import json
import os

HIGH_SCORE_FILE = "high_score.json"

def load_high_score():
    """Load the high score from file, return 0 if file doesn't exist"""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            return 0
    return 0

def save_high_score(score):
    """Save the high score to file"""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': score}, f)
    except IOError:
        pass  # Silently fail if we can't write

def update_high_score(score):
    """Update high score if the new score is higher"""
    current_high = load_high_score()
    if score > current_high:
        save_high_score(score)
        return True
    return False

