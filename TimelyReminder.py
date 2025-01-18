"""
Sends periodic reminders to players.
Tracks playtime and reminds players to take breaks at specified intervals (default: 30 minutes).
Supports custom reminders and a maximum number of reminders (default: 5).
Endpoints: `/start_game_timer` (POST) and `/get_reminders` (GET).
Uses threading for asynchronous reminder delivery.
"""

from flask import Flask, jsonify, request
import time
import threading

app = Flask(__name__)

user_timers = {}

def reminder_message(play_duration_minutes):
    hours, minutes = divmod(play_duration_minutes, 60)
    if hours > 0:
        return f"It's been {hours} hour(s) and {minutes} minute(s) since you started playing. Take a break and go for a walk around the nature!!!"
    else:
        return f"It's been {minutes} minute(s) since you started playing. Take a break and go for a walk around the nature!!!"
        

def game_play_timer(user_id, reminder_interval_minutes, max_reminders, custom_message=None):
    start_time = time.time()
    reminder_count = 0
    reminders = []

    while reminder_count < max_reminders:
        time.sleep(reminder_interval_minutes * 60)
        elapsed_time = (time.time() - start_time) / 60
        reminder_msg = custom_message if custom_message else reminder_message(elapsed_time)
        reminders.append(reminder_msg)
        reminder_count += 1

    reminders.append("\nGame play reminder limit reached. Please consider taking a break or exiting the game.")
    user_timers[user_id]["reminders"] = reminders
    user_timers[user_id]["status"] = "completed"

@app.route('/start_game_timer', methods=['POST'])
def start_game_timer():
    user_id = request.json.get('user_id')
    reminder_interval_minutes = request.json.get('interval', 30)
    max_reminders = request.json.get('max_reminders', 5)
    custom_message = request.json.get('custom_message')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    if reminder_interval_minutes <= 0 or max_reminders <= 0:
        return jsonify({"error": "Interval and max reminders must be positive integers"}), 400

    if user_id in user_timers:
        return jsonify({"error": "A timer is already running for this user"}), 400

    user_timers[user_id] = {
        "status": "running",
        "start_time": time.time(),
        "reminders": []
    }

    timer_thread = threading.Thread(
        target=game_play_timer,
        args=(user_id, reminder_interval_minutes, max_reminders, custom_message)
    )
    timer_thread.start()

    return jsonify({
        "message": "Game timer started successfully.",
        "user_id": user_id,
        "interval_minutes": reminder_interval_minutes,
        "max_reminders": max_reminders,
        "custom_message": custom_message
    })

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    if user_id not in user_timers:
        return jsonify({"error": "No timer found for this user"}), 404

    return jsonify({
        "user_id": user_id,
        "status": user_timers[user_id]["status"],
        "reminders": user_timers[user_id]["reminders"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
