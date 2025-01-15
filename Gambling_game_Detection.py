"""
Flask API to detect if a game involves gambling based on metadata.
three key indicators: betting/wagering, randomness, and rewards.
Returns whether the game is gambling and handles invalid or missing metadata.
Endpoint: `/detect_gambling_game`
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

class GamblingDetectionAPI:
    def __init__(self):
        self.required_keys = ["has_bet_or_wager", "has_randomness", "has_rewards"]

    def validate_metadata(self, metadata):
        for key in self.required_keys:
            if key not in metadata:
                return False, f"Missing required metadata key: {key}"
            if not isinstance(metadata[key], bool):
                return False, f"Invalid value for key '{key}'. Expected a boolean."
        return True, "Metadata is valid"

    def is_gambling_game(self, metadata):
        is_valid, error_message = self.validate_metadata(metadata)
        if not is_valid:
            raise ValueError(error_message)

        has_bet_or_wager = metadata.get("has_bet_or_wager", False)
        has_randomness = metadata.get("has_randomness", False)
        has_rewards = metadata.get("has_rewards", False)

        return has_bet_or_wager and has_randomness and has_rewards

@app.route('/detect_gambling_game', methods=['POST'])
def detect_gambling_game_api():
    data = request.get_json()
    
    if 'metadata' not in data:
        return jsonify({"error": "Game metadata is required"}), 400
    
    metadata = data['metadata']
    gambling_detector = GamblingDetectionAPI()
    
    try:
        is_gambling = gambling_detector.is_gambling_game(metadata)
        return jsonify({
            "is_gambling_game": is_gambling,
            "message": "Gambling detection completed successfully."
        })
    except ValueError as e:
        return jsonify({
            "error": str(e),
            "is_gambling_game": False,
            "message": "Gambling detection failed due to invalid metadata."
        }), 400

if __name__ == "__main__":
    app.run(debug=True)
