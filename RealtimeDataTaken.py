"""
Flask API to monitor system resource usage in real-time.
Tracks camera, microphone, photos access, CPU, and memory usage.
Endpoint: /status.
Uses threading for continuous system resource monitoring.
Supports cross-platform.
"""
import os
import psutil
import cv2
import pyaudio
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

resource_status = {
    "camera": "Not in use",
    "microphone": "Not in use",
    "photos": "Not in use",
    "cpu_usage": "0%",
    "memory_usage": "0%"
}

def check_camera_usage():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        resource_status["camera"] = "Camera is being used"
    else:
        resource_status["camera"] = "Camera is not in use"
    cap.release()

def check_microphone_usage():
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0 and "microphone" in device_info["name"].lower():
            resource_status["microphone"] = "Microphone is being used"
            break
    else:
        resource_status["microphone"] = "Microphone is not in use"

def check_photos_access():
    photos_dir = os.path.expanduser("~/Pictures")
    if os.path.exists(photos_dir):
        recent_files = sorted(
            [os.path.join(photos_dir, f) for f in os.listdir(photos_dir)],
            key=os.path.getmtime,
            reverse=True
        )
        if recent_files:
            resource_status["photos"] = f"Photos accessed recently: {recent_files[0]}"
        else:
            resource_status["photos"] = "No recent photo access"
    else:
        resource_status["photos"] = "Photos directory not found"

def check_system_resources():
    while True:
        resource_status["cpu_usage"] = f"{psutil.cpu_percent()}%"
        resource_status["memory_usage"] = f"{psutil.virtual_memory().percent}%"
        time.sleep(5)

@app.route('/status', methods=['GET'])
def get_status():
    check_camera_usage()
    check_microphone_usage()
    check_photos_access()
    return jsonify(resource_status)

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=check_system_resources)
    monitor_thread.daemon = True
    monitor_thread.start()
    app.run(host="0.0.0.0", port=5000)
