"""
Flask API to filter swear words from input text. Replaces swear words with '***'
Endpoint: /filter_swear_words
Validates input and returns filtered text with a success message.
Needs a CSV file (`harshwords.txt`) containing swear words.
"""
from flask import Flask, request, jsonify
import pandas as pd
import re
import os

app = Flask(__name__)

def load_swear_words(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Swear words file not found: {file_path}")
    df = pd.read_csv(file_path)
    return set(df['Sentences'].str.lower().str.strip())

def create_swear_patterns(swear_words):
    patterns = []
    for word in swear_words:
        escaped_word = re.escape(word)
        pattern = r'\b' + escaped_word.replace('', r'[\-\*0-9]*') + r'\b'
        patterns.append(pattern)
    return re.compile('|'.join(patterns), re.IGNORECASE)

def filter_swear_words(input_text, swear_pattern):
    return swear_pattern.sub('***', input_text)

@app.route('/filter_swear_words', methods=['POST'])
def filter_swear_words_api():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "Text field is required"}), 400

    input_text = data['text']
    filtered_text = filter_swear_words(input_text, swear_pattern)
    return jsonify({
        "filtered_text": filtered_text,
        "message": "Swear words filtered successfully."
    })

if __name__ == "__main__":
    swear_words_file = "harshwords.txt"
    try:
        swear_words_set = load_swear_words(swear_words_file)
        swear_pattern = create_swear_patterns(swear_words_set)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    app.run(debug=True)
