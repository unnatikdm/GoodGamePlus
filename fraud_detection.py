"""
Flask API for user verification and gift sending.
Verifies users via facial recognition using ID and selfie photos.
Approves users for sending gifts if verification is successful.
Supports random hand emoji conditions
Endpoints: /verify (POST), /send_gift (POST).
"""

from flask import Flask, request, jsonify
import cv2
import face_recognition
import numpy as np
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_id(id_photo_path):
    if os.path.exists(id_photo_path):
        return True
    return False

def verify_selfie(id_photo_path, selfie_path):
    if not selfie_path:
        return False

    id_image = face_recognition.load_image_file(id_photo_path)
    selfie_image = face_recognition.load_image_file(selfie_path)

    try:
        id_face_encoding = face_recognition.face_encodings(id_image)[0]
        selfie_face_encoding = face_recognition.face_encodings(selfie_image)[0]
    except IndexError:
        return False

    results = face_recognition.compare_faces([id_face_encoding], selfie_face_encoding)
    return results[0]

def get_random_hand_emoji():
    hand_emojis = ["✌🏻", "👌🏻", "🤘🏻", "🤙🏻", "🖖🏻", "🤞🏻", "👊🏻", "👍🏻", "👎🏻", "✊🏻"]
    return random.choice(hand_emojis)

@app.route("/verify", methods=["POST"])
def verify_user():
    if "id_photo" not in request.files or "selfie" not in request.files:
        return jsonify({"error": "ID photo and selfie are required"}), 400

    id_photo = request.files["id_photo"]
    selfie = request.files["selfie"]

    if not allowed_file(id_photo.filename) or not allowed_file(selfie.filename):
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed"}), 400

    id_photo_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(id_photo.filename))
    selfie_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(selfie.filename))
    id_photo.save(id_photo_path)
    selfie.save(selfie_path)

    if not verify_id(id_photo_path):
        return jsonify({"error": "ID verification failed"}), 400

    condition = get_random_hand_emoji()

    if not verify_selfie(id_photo_path, selfie_path):
        return jsonify({"error": "Selfie verification failed"}), 400

    return jsonify({
        "message": "Verification successful",
        "condition": condition,
        "status": "approved"
    }), 200

@app.route("/send_gift", methods=["POST"])
def send_gift():
    data = request.json
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    condition = data.get("condition")
    is_approved = data.get("is_approved")

    if not sender_id or not receiver_id or not condition or is_approved is None:
        return jsonify({"error": "Sender ID, receiver ID, condition, and approval status are required"}), 400

    if not is_approved:
        return jsonify({"error": "Sender is not approved to send gifts"}), 403

    print(f"Sender {sender_id} is sending a gift to receiver {receiver_id} with condition: {condition}")
    return jsonify({
        "message": "Gift sent successfully",
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "condition": condition
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
