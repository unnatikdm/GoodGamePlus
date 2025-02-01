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
import getpass  # For password input in the terminal
import os  # For os._exit() to forcefully exit the application

app = Flask(__name__)

# Store user timers and reminders in a dictionary
user_timers = {}

# Hardcoded user data and settings
user_id = "player1"
reminder_interval_seconds = 2  # 2 seconds for faster testing
max_reminders = 3  # 3 reminders max
custom_message = "Take a break and stretch your legs!"
password = "securePassword"  # Define the password to check after 3 reminders

# Default reminder message
def reminder_message(play_duration_seconds):
    minutes, seconds = divmod(play_duration_seconds, 60)
    if minutes > 0:
        return f"It's been {minutes} minute(s) and {seconds} second(s) since you started playing. {custom_message}"
    else:
        return f"It's been {seconds} second(s) since you started playing. {custom_message}"

# Function to ask for a password after 3 reminders
def ask_for_password():
    user_input = getpass.getpass("Enter the password to continue: ")
    if user_input != password:
        print("Incorrect password. Exiting...")
        shutdown_flask()  # Call the function to shut down Flask if password is incorrect
    else:
        print("Password correct. Continuing...")

# Function to forcefully exit the Flask server
def shutdown_flask():
    print("Shutting down the server...")
    os._exit(0)  # Exit the program immediately

# The function that runs the timer and sends periodic reminders
def game_play_timer(user_id, reminder_interval_seconds, max_reminders, custom_message=None):
    start_time = time.time()  # Track the start time
    reminder_count = 0
    reminders = []  # List to store all reminders for the user

    while True:
        while reminder_count < max_reminders:
            time.sleep(reminder_interval_seconds)  # Wait for the interval time

            # Calculate elapsed time in seconds
            elapsed_time = (time.time() - start_time)

            # Use custom message if provided, else use default
            reminder_msg = custom_message if custom_message else reminder_message(elapsed_time)
            reminders.append(reminder_msg)  # Add reminder to list
            reminder_count += 1

            # Print the reminder message to the console
            print(reminder_msg)

            # Save the current reminders in the user_timers dictionary
            user_timers[user_id]["reminders"] = reminders

        # After max reminders, ask for password and check it
        print("Reminder limit reached. Please enter the password to continue...")

        # Start a separate thread to handle password input without blocking Flask
        password_thread = threading.Thread(target=ask_for_password)
        password_thread.start()
        password_thread.join()  # Wait for the password check to finish

        # Reset reminder count and start again
        reminder_count = 0
        reminders = []  # Reset the reminders for the next round
        user_timers[user_id]["reminders"] = reminders

        # Optionally, you can reset the game timer start_time if needed for the new round
        start_time = time.time()

@app.route('/start_game_timer', methods=['POST'])
def start_game_timer():
    # Initialize the user timer with hardcoded data
    user_timers[user_id] = {
        "status": "running",
        "start_time": time.time(),
        "reminders": []
    }

    # Start the timer in a separate thread
    timer_thread = threading.Thread(
        target=game_play_timer,
        args=(user_id, reminder_interval_seconds, max_reminders, custom_message)
    )
    timer_thread.daemon = True  # Allow the thread to run in the background
    timer_thread.start()

    return jsonify({
        "message": "Game timer started successfully.",
        "user_id": user_id,
        "interval_seconds": reminder_interval_seconds,
        "max_reminders": max_reminders,
        "custom_message": custom_message
    })

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    # Fetch the reminders for the hardcoded user_id
    if user_id not in user_timers:
        return jsonify({"error": "No timer found for this user"}), 404

    return jsonify({
        "user_id": user_id,
        "status": user_timers[user_id]["status"],
        "reminders": user_timers[user_id]["reminders"]
    })

if __name__ == "__main__":
    # Ensure the app context is available
    with app.app_context():
        # Manually start the timer when the app runs (this is the key fix)
        start_game_timer()

    # Start the Flask app
    app.run(host="0.0.0.0", port=5000)

