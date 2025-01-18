Here’s a **README.md** file that includes all the information you provided, along with details about `fraud_detection.py`. This README is comprehensive and covers all the files in your project.

---

# **SafeGamingApi**

SafeGamingApi is a collection of Flask-based APIs designed to enhance the safety, security, and transparency of gaming environments. The suite includes tools for monitoring game file integrity, detecting threats in voice chat, sending timely reminders to players, monitoring system resources, filtering swear words, detecting gambling elements in games, encrypting sensitive data, and preventing fraud.

---

## **Features**

### 1. **Game File Integrity Monitoring**
   - **File**: `Game_transparency.py`
   - **Description**: Monitors the integrity of critical game files and checks if they exist.
   - **Endpoint**: `/status` (GET)
   - **Customization**: Set `GAME_FILES_DIR` and `critical_files` to match your game's directory and critical files.

---

### 2. **Voice Threat Detection**
   - **File**: `Voice_Threat_Detection.py`
   - **Description**: Preprocesses and balances a dataset of labeled sentences, uses a Sentence Transformer model to encode sentences, and calculates cosine similarity for threat detection. Supports real-time voice input for threat detection.
   - **Features**:
     - Dataset loading and cleaning
     - Dataset balancing
     - Bulk and real-time threat detection
     - Evaluation metrics (accuracy, precision, recall)
     - Misclassified examples export

---

### 3. **Timely Reminders**
   - **File**: `TimelyReminder.py`
   - **Description**: Sends periodic reminders to players to take breaks. Tracks playtime and supports custom reminders.
   - **Endpoints**:
     - `/start_game_timer` (POST): Starts a timer for a user.
     - `/get_reminders` (GET): Retrieves reminders for a user.
   - **Customization**: Set `reminder_interval_minutes` and `max_reminders`.

---

### 4. **Real-Time System Resource Monitoring**
   - **File**: `RealtimeDataTaken.py`
   - **Description**: Monitors system resource usage in real-time, including camera, microphone, photos access, CPU, and memory usage.
   - **Endpoint**: `/status` (GET)
   - **Features**: Cross-platform support, continuous monitoring via threading.

---

### 5. **Swear Words Filtering**
   - **File**: `HarshwordsEncryption.py`
   - **Description**: Filters swear words from input text and replaces them with '***'.
   - **Endpoint**: `/filter_swear_words` (POST)
   - **Requirements**: A CSV file (`harshwords.txt`) containing swear words.

---

### 6. **Gambling Game Detection**
   - **File**: `Gambling_game_Detection.py`
   - **Description**: Detects if a game involves gambling based on metadata. Checks for betting/wagering, randomness, and rewards.
   - **Endpoint**: `/detect_gambling_game` (POST)
   - **Features**: Handles invalid or missing metadata.

---

### 7. **Data Encryption**
   - **File**: `DataEncryption.py`
   - **Description**: Encrypts and decrypts data using the `cryptography.fernet` library. Supports JSON, text, and files.
   - **Endpoints**:
     - `/encrypt` (POST): Encrypts data or files.
     - `/decrypt` (POST): Decrypts data or files.
   - **Features**: Base64 encoding of encrypted data, automatic key generation.

---

### 8. **Fraud Detection**
   - **File**: `fraud_detection.py`
   - **Description**: Verifies users via facial recognition using ID and selfie photos. Approves users for sending gifts if verification is successful. Includes a random hand emoji condition for added security.
   - **Endpoints**:
     - `/verify` (POST): Verifies a user by comparing their ID photo with a selfie.
     - `/send_gift` (POST): Allows an approved user to send a gift.
   - **Features**:
     - Facial recognition for user verification.
     - Random hand emoji condition.
     - Prevents unauthorized gift sending.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SafeGamingApi.git
   cd SafeGamingApi
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the desired API script:
   ```bash
   python Game_transparency.py
   ```

---

## **Usage**

Each API script can be run independently. Refer to the individual script documentation for specific usage instructions and endpoint details.

---

## **Requirements**

- Python 3.7+
- Flask
- pandas
- sentence-transformers
- scikit-learn
- speechrecognition
- psutil
- opencv-python
- pyaudio
- cryptography
- face_recognition

---

## **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## **Acknowledgments**

- Flask for providing a lightweight web framework.
- Sentence Transformers for powerful sentence embeddings.
- Cryptography library for secure data encryption.
- Face Recognition library for facial verification.

---

## **File Descriptions**

| **File**                     | **Description**                                                                 |
|-------------------------------|---------------------------------------------------------------------------------|
| `Game_transparency.py`        | Monitors game file integrity and checks if critical files exist.                |
| `Voice_Threat_Detection.py`   | Detects threats in voice chat using sentence embeddings and cosine similarity.  |
| `TimelyReminder.py`           | Sends periodic reminders to players to take breaks.                             |
| `RealtimeDataTaken.py`        | Monitors system resource usage in real-time.                                    |
| `HarshwordsEncryption.py`     | Filters swear words from input text.                                            |
| `Gambling_game_Detection.py`  | Detects gambling elements in games based on metadata.                           |
| `DataEncryption.py`           | Encrypts and decrypts data using the Fernet algorithm.                          |
| `fraud_detection.py`          | Verifies users via facial recognition and prevents unauthorized gift sending.   |
| `README.md`                   | Documentation for the SafeGamingApi project.                                    |
| `hate_speech.tsv`             | Dataset for hate speech detection (used in `Voice_Threat_Detection.py`).        |
| `mainxlsx.xlsx`               | Dataset for threat detection (used in `Voice_Threat_Detection.py`).             |

---

## **Example Requests**

### **Fraud Detection API**
1. **Verify a User**:
   ```bash
   curl -X POST -F "id_photo=@id.jpg" -F "selfie=@selfie.jpg" http://0.0.0.0:5000/verify
   ```

2. **Send a Gift**:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
       "sender_id": "123",
       "receiver_id": "456",
       "condition": "✌🏻",
       "is_approved": true
   }' http://0.0.0.0:5000/send_gift
   ```

---

## **Future Enhancements**
1. **Database Integration**:
   - Store user verification results and gift transactions in a database.
2. **Multi-Factor Authentication**:
   - Add additional verification steps (e.g., OTP, email confirmation).
3. **Rate Limiting**:
   - Prevent abuse by limiting the number of verification attempts.

---

This README provides a complete overview of your project, including all files and their functionalities. Let me know if you need further adjustments!
