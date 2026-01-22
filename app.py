from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

class NeuralFootAI:
    def __init__(self):
        self.model_version = "NeuralFoot AI v3.6 PythonAnywhere Ready"
    
    def get_demo_matches(self):
        return {
            "fixtures": [
                {
                    "home_team": "Manchester City",
                    "away_team": "Arsenal",
                    "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "time": "16:30",
                    "league": "Premier League",
                    "home_odds": 2.1,
                    "draw_odds": 3.4,
                    "away_odds": 3.2
                },
                {
                    "home_team": "Real Madrid",
                    "away_team": "Barcelona",
                    "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "time": "20:00",
                    "league": "La Liga",
                    "home_odds": 1.9,
                    "draw_odds": 3.6,
                    "away_odds": 3.8
                },
                {
                    "home_team": "Bayern Munich",
                    "away_team": "Borussia Dortmund",
                    "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    "time": "18:30",
                    "league": "Bundesliga",
                    "home_odds": 1.5,
                    "draw_odds": 4.2,
                    "away_odds": 6.0
                },
                {
                    "home_team": "AC Milan",
                    "away_team": "Inter Milan",
                    "date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
                    "time": "19:45",
                    "league": "Serie A",
                    "home_odds": 2.8,
                    "draw_odds": 3.2,
                    "away_odds": 2.6
                },
                {
                    "home_team": "Paris Saint-Germain",
                    "away_team": "Olympique Lyon",
                    "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "time": "21:00",
                    "league": "Ligue 1",
                    "home_odds": 1.4,
                    "draw_odds": 4.5,
                    "away_odds": 7.0
                }
            ]
        }
    
    def calculate_prediction(self, match):
        home_odds = float(match.get('home_odds', 2.0))
        draw_odds = float(match.get('draw_odds', 3.0))
        away_odds = float(match.get('away_odds', 3.0))
        
        # Convert odds to probabilities
        home_prob = 1 / home_odds
        draw_prob = 1 / draw_odds
        away_prob = 1 / away_odds
        
        # Normalize
        total = home_prob + draw_prob + away_prob
        home_prob /= total
        draw_prob /= total
        away_prob /= total
        
        # Add realistic variance
        home_prob += random.uniform(-0.05, 0.05)
        draw_prob += random.uniform(-0.03, 0.03)
        away_prob += random.uniform(-0.05, 0.05)
        
        # Final determination
        rand = random.random()
        if rand < home_prob:
            result = "Home Win"
            confidence = int(home_prob * 100)
        elif rand < home_prob + draw_prob:
            result = "Draw"
            confidence = int(draw_prob * 100)
        else:
            result = "Away Win"
            confidence = int(away_prob * 100)
        
        return {
            'result': result,
            'confidence': min(confidence, 85),
            'probabilities': {
                'home': round(home_prob * 100, 1),
                'draw': round(draw_prob * 100, 1),
                'away': round(away_prob * 100, 1)
            },
            'expected_goals': {
                'home': round(random.uniform(1.2, 2.8), 1),
                'away': round(random.uniform(0.8, 2.2), 1)
            }
        }
    
    def get_matches_with_predictions(self):
        api_data = self.get_demo_matches()
        matches = []
        
        for match in api_data['fixtures']:
            match_with_prediction = {
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'date': match['date'],
                'time': match['time'],
                'league': match['league'],
                'prediction': self.calculate_prediction(match),
                'timestamp': datetime.now().isoformat(),
                'model_version': self.model_version
            }
            matches.append(match_with_prediction)
        
        return matches

ai_predictor = NeuralFootAI()

@app.route('/')
def home():
    return jsonify({
        'service': 'NeuralFoot AI - PythonAnywhere Ready',
        'version': '3.6',
        'status': 'active',
        'platform': 'Local → PythonAnywhere'
    })

@app.route('/api/matches')
def get_matches():
    try:
        matches = ai_predictor.get_matches_with_predictions()
        return jsonify({
            'status': 'success',
            'count': len(matches),
            'matches': matches,
            'generated_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'neuralfoot-ai-clean'
    })

# Local testing entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
