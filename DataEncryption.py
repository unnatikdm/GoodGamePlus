
"""
This allows the encryption and decryption of data provided by the user. 
The API supports various types of input, including structured data (JSON), strings, 
binary data, images, videos, and other files. 
The encrypted data can be decrypted 
using the same key that is generated during the encryption process.
"""
import os
import json
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    file = request.files.get('file')
    data = request.form.get('data')
    user_key = request.form.get('key')

    if not (data or file):
        return jsonify({"error": "No data or file provided for encryption"}), 400

    if user_key:
        try:
            cipher = Fernet(user_key.encode())
        except Exception as e:
            return jsonify({"error": "Invalid key provided"}), 400
    else:
        key = Fernet.generate_key()
        cipher = Fernet(key)

    if file:
        encrypted_chunks = []
        while chunk := file.stream.read(4096):
            encrypted_chunks.append(cipher.encrypt(chunk))
        encrypted_data = b"".join(encrypted_chunks)
    else:
        input_type = detect_input_type(data)
        encrypted_data = encrypt_unknown_input(data, input_type, cipher)

    response = {
        "encrypted_data": base64.b64encode(encrypted_data).decode(),
    }
    if not user_key:
        response["key"] = key.decode()

    return jsonify(response)

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    encrypted_data = request.get_json().get("encrypted_data")
    user_key = request.get_json().get("key")

    if not encrypted_data or not user_key:
        return jsonify({"error": "Encrypted data and key are required for decryption"}), 400

    try:
        cipher = Fernet(user_key.encode())
        encrypted_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = decrypt_unknown_input(encrypted_data, cipher)
    except Exception as e:
        return jsonify({"error": "Decryption failed. Invalid key or data."}), 400

    return jsonify({
        "decrypted_data": decrypted_data
    })

def detect_input_type(data):
    if isinstance(data, str):
        try:
            json.loads(data)
            return "structured"
        except json.JSONDecodeError:
            return "string"
    else:
        return "string"

def encrypt_unknown_input(data, input_type, cipher):
    if input_type == "structured":
        serialized_data = json.dumps(data).encode()
        return cipher.encrypt(serialized_data)
    elif input_type == "string":
        return cipher.encrypt(data.encode())
    else:
        raise ValueError("Unsupported input type for encryption.")

def decrypt_unknown_input(encrypted_data, cipher):
    decrypted_data = cipher.decrypt(encrypted_data)
    try:
        return json.loads(decrypted_data.decode())
    except json.JSONDecodeError:
        try:
            return decrypted_data.decode()
        except UnicodeDecodeError:
            return "Binary data could not be decoded."

if __name__ == "__main__":
    app.run(debug=True)
