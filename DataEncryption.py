
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

app = Flask(__name__)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    data = request.get_json().get("data")
    if not data:
        return jsonify({"error": "No data provided for encryption"}), 400
    
    input_type = detect_input_type(data)
    encrypted_data = encrypt_unknown_input(data)
    
    return jsonify({
        "encrypted_data": encrypted_data.decode(),
        "key": key.decode()
    })

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    encrypted_data = request.get_json().get("encrypted_data")
    if not encrypted_data:
        return jsonify({"error": "No encrypted data provided for decryption"}), 400
    
    encrypted_data = encrypted_data.encode()
    decrypted_data = decrypt_unknown_input(encrypted_data)
    
    return jsonify({
        "decrypted_data": decrypted_data
    })

def detect_input_type(data):
    if isinstance(data, (dict, list)):
        return "structured"
    elif isinstance(data, str):
        try:
            json.loads(data)
            return "structured"
        except json.JSONDecodeError:
            return "string"
    elif isinstance(data, bytes):
        return "binary"
    elif os.path.isfile(data):
        ext = os.path.splitext(data)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            return "image"
        elif ext in [".mp4", ".avi", ".mov"]:
            return "video"
        else:
            return "file"
    else:
        raise ValueError("Unsupported input type.")

def encrypt_unknown_input(data):
    input_type = detect_input_type(data)
    if input_type == "structured":
        serialized_data = json.dumps(data).encode()
        return cipher.encrypt(serialized_data)
    elif input_type == "string":
        return cipher.encrypt(data.encode())
    elif input_type == "binary":
        return cipher.encrypt(data)
    elif input_type in ["image", "video", "file"]:
        with open(data, "rb") as file:
            binary_data = file.read()
        return cipher.encrypt(binary_data)
    else:
        raise ValueError("Unsupported input type for encryption.")

def decrypt_unknown_input(encrypted_data, output_path=None, is_binary=False):
    decrypted_data = cipher.decrypt(encrypted_data)
    if is_binary or output_path:
        if output_path:
            with open(output_path, "wb") as file:
                file.write(decrypted_data)
            return f"Decrypted data saved to {output_path}"
        return decrypted_data
    try:
        return json.loads(decrypted_data.decode())
    except json.JSONDecodeError:
        return decrypted_data.decode()

if __name__ == "__main__":
    app.run(debug=True)
