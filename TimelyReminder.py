"""
This a game play reminder system. It sends periodic reminders to the player
after a specified interval (default 30 minutes). It tracks the time elapsed since the game started 
and reminds the player to take breaks after a certain period of play. The player will receive up to 
a maximum number of reminders (default 5).
"""
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

def reminder_message(play_duration_minutes):
    hours, minutes = divmod(play_duration_minutes, 60)
    if hours > 0:
        return f"It's been {hours} hour(s) and {minutes} minute(s) since you started playing. Take a break if needed!"
    else:
        return f"It's been {minutes} minute(s) since you started playing. Time flies!"

def game_play_timer(reminder_interval_minutes=30, max_reminders=5):
    start_time = time.time()
    reminder_count = 0
    reminders = []

    while reminder_count < max_reminders:
        time.sleep(reminder_interval_minutes * 60)
        elapsed_time = (time.time() - start_time) / 60
        reminder_msg = reminder_message(elapsed_time)
        reminders.append(reminder_msg)
        reminder_count += 1

    reminders.append("\nGame play reminder limit reached. Please consider taking a break or exiting the game.")
    return reminders

@app.route('/start_game_timer', methods=['GET'])
def start_game_timer():
    reminder_interval_minutes = request.args.get('interval', default=30, type=int)
    max_reminders = request.args.get('max_reminders', default=5, type=int)
    reminders = game_play_timer(reminder_interval_minutes, max_reminders)
    return jsonify({"reminders": reminders})

if __name__ == "__main__":
    app.run(debug=True)
