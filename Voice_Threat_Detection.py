"""
It preprocesses and balances a dataset of labeled sentences. 
Uses a Sentence Transformer model to encode the sentences and calculate cosine similarity for threat detection.
Includes evaluation metrics (accuracy, precision, recall) and exports misclassified examples.
Supports real-time voice input for threat detection via speech recognition
"""
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr
import os
from sklearn.utils import resample


def load_and_clean_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    data = pd.read_excel(file_path)
    data['sentences'] = data['sentences'].fillna("").astype(str)
    data['labels'] = data['labels'].str.strip().str.lower()
    return data


def balance_dataset(data):
    threat_data = data[data['labels'] == 'yes']
    non_threat_data = data[data['labels'] == 'no']
    threat_data_upsampled = resample(threat_data, replace=True, n_samples=len(non_threat_data), random_state=42)
    balanced_data = pd.concat([threat_data_upsampled, non_threat_data]).sample(frac=1, random_state=42)
    return balanced_data


def detect_threat_from_voice(input_text, threat_sentences, model, threshold=0.7):
    input_embedding = model.encode([input_text], show_progress_bar=False)
    similarities = cosine_similarity(input_embedding, threat_sentences)
    is_threat = max(similarities[0]) > threshold
    return 'Yes' if is_threat else 'No'


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Speak now:")
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)
            return recognizer.recognize_google(audio, language='en-IN')
        except Exception as e:
            print(f"Error processing voice input: {e}")
            return None


def test_single_sentence_with_voice(threat_sentences, model, threshold=0.85):
    input_text = get_voice_input()
    if not input_text:
        print("Couldn't process your input. Please try again.")
        return
    print(f"Input Sentence: {input_text}")
    threat_status = detect_threat_from_voice(input_text, threat_sentences, model, threshold)
    print(f"Threat Detected: {threat_status}")


    if threat_status == 'Yes':
        user_response = input("A system detected a threat. Are you comfortable or is it normal? (Type 'comfortable' or 'normal'): ").strip().lower()
        if user_response == "comfortable":
            print("Noted. You feel comfortable.")
        elif user_response == "normal":
            print("Noted. It is considered normal.")
        else:
            print("Invalid response. Proceeding with default settings.")

if __name__ == "__main__":
    dataset_path = "C:\\Users\\Isha\\Downloads\\SafeGamingAPI-main\\SafeGamingAPI-main\\mainxlsx.xlsx"  # Provide the actual path to your dataset file
    
    try:
        data = load_and_clean_dataset(dataset_path)
        balanced_data = balance_dataset(data)
        threat_sentences = balanced_data[balanced_data['labels'] == 'yes']['sentences'].tolist()

        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        threat_embeddings = model.encode(threat_sentences, batch_size=16, show_progress_bar=False)

        # Run the real-time voice threat detection
        print("Running real-time threat detection...")
        test_single_sentence_with_voice(threat_embeddings, model, threshold=0.75)

    except Exception as e:
        print(f"An error occurred: {e}")
