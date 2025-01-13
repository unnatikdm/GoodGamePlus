"""
This provides a service to detect whether a game involves gambling based on its metadata.
The game is considered gambling if it includes betting, randomness, and rewards.
If any of the necessary metadata is missing, it could indicate a potential threat or incomplete data.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

class GamblingDetectionAPI:
  
    def __init__(self):
        pass

    def is_gambling_game(self, metadata):
      
        required_keys = ["has_bet_or_wager", "has_randomness", "has_rewards"]
        for key in required_keys:
            if key not in metadata:
                raise ValueError(f"Missing required metadata key: {key}. This could be a potential threat.")

        has_bet_or_wager = metadata.get("has_bet_or_wager", False)
        has_randomness = metadata.get("has_randomness", False)
        has_rewards = metadata.get("has_rewards", False)

        if not has_bet_or_wager or not has_randomness or not has_rewards:
            raise ValueError("Incomplete metadata. The game could potentially have gambling or other risks.")

        if has_bet_or_wager and has_randomness and has_rewards:
            return True
        return False

@app.route('/detect_gambling_game', methods=['POST'])
def detect_gambling_game_api():
    
    data = request.get_json()
    
    if 'metadata' not in data:
        return jsonify({"error": "Game metadata is required"}), 400
    
    metadata = data['metadata']
    
    gambling_detector = GamblingDetectionAPI()
    
    try:
        is_gambling = gambling_detector.is_gambling_game(metadata)
        return jsonify({"is_gambling_game": is_gambling})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
