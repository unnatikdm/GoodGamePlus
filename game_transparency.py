"""
Flask API to monitor game file integrity and checks if critical files exist.
Endpoint: `/status` (GET) 
Customize `GAME_FILES_DIR` and `critical_files` for your game.
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

GAME_FILES_DIR = ///put the director path of the game

def check_file_integrity():
    results = {}
    critical_files = ["game.exe", "config.ini"] 
    for file_name in critical_files:
        file_path = os.path.join(GAME_FILES_DIR, file_name)
        if not os.path.exists(file_path):
            results[file_name] = "File not found"
        else:
            results[file_name] = "File exists"
    return results

@app.route('/status', methods=['GET'])
def get_status():
    file_integrity = check_file_integrity()
    return jsonify({
        "file_integrity_checks": file_integrity
    })

if __name__ == "__main__":
    app.run(debug=True)
