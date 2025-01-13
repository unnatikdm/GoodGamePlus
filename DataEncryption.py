
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
    # If the input is a file, it will come through request.files
    file = request.files.get('file')
    data = request.form.get('data')  # For structured data like strings or JSON
    
    if not (data or file):
        return jsonify({"error": "No data or file provided for encryption"}), 400
    
    if file:
        # Encrypt file data
        encrypted_data = encrypt_unknown_input(file.read(), 'binary')
        return jsonify({
            "encrypted_data": encrypted_data.decode(),
            "key": key.decode()
        })
    
    input_type = detect_input_type(data)
    encrypted_data = encrypt_unknown_input(data, input_type)
    
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
    if isinstance(data, str):
        try:
            json.loads(data)  # Try to load as JSON
            return "structured"
        except json.JSONDecodeError:
            return "string"
    else:
        return "string"

def encrypt_unknown_input(data, input_type):
    if input_type == "structured":
        serialized_data = json.dumps(data).encode()
        return cipher.encrypt(serialized_data)
    elif input_type == "string":
        return cipher.encrypt(data.encode())
    elif input_type == "binary":
        return cipher.encrypt(data)
    else:
        raise ValueError("Unsupported input type for encryption.")

def decrypt_unknown_input(encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data)
    
    try:
        # Try to parse as JSON
        return json.loads(decrypted_data.decode())
    except json.JSONDecodeError:
        # If not JSON, return as plain text or binary
        try:
            return decrypted_data.decode()  # Return plain text if it's a string
        except UnicodeDecodeError:
            return "Binary data could not be decoded."

if __name__ == "__main__":
    app.run(debug=True)
