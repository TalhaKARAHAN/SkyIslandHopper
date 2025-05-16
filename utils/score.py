import json
import os

def load_high_score():
    try:
        if os.path.exists('highscore.json'):
            with open('highscore.json', 'r') as f:
                return json.load(f)['high_score']
    except:
        pass
    return 0

def save_high_score(high_score):
    try:
        with open('highscore.json', 'w') as f:
            json.dump({'high_score': high_score}, f)
    except:
        pass 