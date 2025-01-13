"""
This script provides a Flask API that filters out swear words and their common variations from input text.
The API endpoint `/filter_swear_words` accepts a POST request with a text payload and returns the filtered text with swear words replaced by '***'.


"""

from flask import Flask, request, jsonify
import pandas as pd
import re

app = Flask(__name__)

def load_swear_words(file_path):
    df = pd.read_csv(file_path)
    return set(df['Sentences'].str.lower().str.strip())

def create_swear_patterns(swear_words):
    patterns = []
    for word in swear_words:
        escaped_word = re.escape(word)
        pattern = re.compile(r'\b' + escaped_word.replace('', r'[\-\*0-9]*') + r'\b', re.IGNORECASE)
        patterns.append(pattern)
    return patterns

def filter_swear_words(input_text, swear_patterns):
    for pattern in swear_patterns:
        input_text = pattern.sub('***', input_text)
    return input_text

@app.route('/filter_swear_words', methods=['POST'])
def filter_swear_words_api():
    data = request.get_json()
    input_text = data['text']
    filtered_text = filter_swear_words(input_text, swear_patterns)
    return jsonify({"filtered_text": filtered_text})

if __name__ == "__main__":
    swear_words_file = '/content/harshwords.txt'  # Replace with your file path
    swear_words_set = load_swear_words(swear_words_file)
    swear_patterns = create_swear_patterns(swear_words_set)
    app.run(debug=True)
