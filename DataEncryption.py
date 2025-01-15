"""
Flask API for encrypting and decrypting data. Supports JSON, text, and files.
Uses cryptography.ferne for data handling.
Endpoints: `/encrypt` and `/decrypt`
Encrypted data is base64-encode
"""

from flask import Flask, request, jsonify
from cryptography.fernet import Fernet, InvalidToken
import base64

app = Flask(__name__)

def is_valid_fernet_key(key):
    try:
        Fernet(key.encode())
        return True
    except (ValueError, InvalidToken):
        return False

def is_valid_base64(data):
    try:
        base64.b64decode(data.encode())
        return True
    except (ValueError, TypeError):
        return False

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    encrypted_data = data.get("encrypted_data")
    user_key = data.get("key")
    if not encrypted_data or not user_key:
        return jsonify({"error": "Both 'encrypted_data' and 'key' are required"}), 400

    if not is_valid_fernet_key(user_key):
        return jsonify({"error": "Invalid Fernet key provided"}), 400

    if not is_valid_base64(encrypted_data):
        return jsonify({"error": "Invalid base64-encoded data provided"}), 400

    try:
        cipher = Fernet(user_key.encode())
        encrypted_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = decrypt_unknown_input(encrypted_data, cipher)
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

    return jsonify({
        "decrypted_data": decrypted_data
    })

def decrypt_unknown_input(encrypted_data, cipher):
    decrypted_data = cipher.decrypt(encrypted_data)
    try:
        return json.loads(decrypted_data.decode())
    except json.JSONDecodeError:
        try:
            return decrypted_data.decode()
        except UnicodeDecodeError:
            return decrypted_data

if __name__ == "__main__":
    app.run(debug=True)
