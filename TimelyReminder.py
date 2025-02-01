"""
This script provides a timer application with two modes: Default Timer and Parental Timer.
The Default Timer sends periodic reminders to take breaks, while the Parental Timer runs for a user-specified duration.
After each timer session, the user is prompted to enter a password to continue or exit.
The application uses Flask to handle HTTP requests and runs in the background while accepting user input in the terminal.
The program loops until the user chooses to exit, supporting multiple rounds of playtime with password verification.
"""
from flask import Flask, jsonify, request
import time
import threading
import getpass  
import os  

app = Flask(__name__)

user_timers = {}

user_id = "player1"
custom_message = "Take a break and stretch your legs!"
password = "securePassword"  

def reminder_message(play_duration_seconds):
    minutes, seconds = divmod(play_duration_seconds, 60)
    if minutes > 0:
        return f"It's been {minutes} minute(s) and {seconds} second(s) since you started playing. {custom_message}"
    else:
        return f"It's been {seconds} second(s) since you started playing. {custom_message}"

def ask_for_password():
    user_input = getpass.getpass("Enter the password to continue: ")
    if user_input != password:
        print("Incorrect password. Exiting...")
        shutdown_flask()
    else:
        print("Password correct. Continuing to the next round...")

def shutdown_flask():
    print("Shutting down the server...")
    os._exit(0)

def game_play_timer_default(user_id, reminder_interval_seconds, max_reminders, custom_message=None):
    if user_id not in user_timers:
        user_timers[user_id] = {"reminders": []}

    start_time = time.time()
    reminder_count = 0
    reminders = []

    while reminder_count < max_reminders:
        time.sleep(reminder_interval_seconds)
        elapsed_time = (time.time() - start_time)
        reminder_msg = custom_message if custom_message else reminder_message(elapsed_time)
        reminders.append(reminder_msg)
        reminder_count += 1
        print(reminder_msg)
        user_timers[user_id]["reminders"] = reminders

    print("Reminder limit reached. Please enter the password to continue...")
    password_thread = threading.Thread(target=ask_for_password)
    password_thread.start()
    password_thread.join()

def game_play_timer_parental(user_id, play_duration_seconds, custom_message=None):
    start_time = time.time()

    while time.time() - start_time < play_duration_seconds:
        time.sleep(1)

    elapsed_time = time.time() - start_time
    reminder_msg = custom_message if custom_message else reminder_message(elapsed_time)
    print(reminder_msg)

    print("Game time finished. Please enter the password to continue.")
    ask_for_password()

def choose_timer():
    while True:
        choice = input("Enter '1' for Default Timer or '2' for Parental Timer: ")
        
        if choice == '1':
            print("Starting Default Timer (Code 1)...")
            reminder_interval_seconds = 2  
            max_reminders = 3  
            game_play_timer_default(user_id, reminder_interval_seconds, max_reminders, custom_message)
        elif choice == '2':
            print("Starting Parental Timer (Code 2)...")
            play_duration_seconds = int(input("How much time do you want to play (in seconds)? "))
            game_play_timer_parental(user_id, play_duration_seconds, custom_message)
        else:
            print("Invalid choice. Please enter '1' or '2'.")

def start_flask_server():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    choose_timer()
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True  
    flask_thread.start()
