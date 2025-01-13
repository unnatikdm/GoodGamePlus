# SafeGamingAPI

# Game Safety and Data Encryption Project

This project includes a suite of tools aimed at improving safety in gaming and ensuring secure handling of user data. The components of the project are designed to address issues such as gambling detection, hate speech filtering, voice threat detection, and time-based reminders during gameplay, along with secure encryption for sensitive data.

## Components

### 1. **DataEncryption.py**
   - This module provides functionality to securely encrypt and decrypt different types of data. It uses `cryptography.fernet` for symmetric encryption. The module handles structured data, strings, binary data, images, videos, and other files, and returns encrypted data that can only be decrypted with the same key.

### 2. **Gambling_game_Detection.py**
   - This module detects whether a game has gambling elements based on the provided metadata. It checks for certain characteristics such as the presence of bets, randomness, and rewards, which are typical indicators of gambling in games.

### 3. **HarshwordsEncryption.py**
   - This module is designed to detect and filter out harsh or offensive words from text inputs. It loads a list of offensive words and uses pattern matching to detect variations of those words, replacing them with asterisks (`***`). This can be used to ensure a safe and respectful environment in online games and chat applications.

### 4. **TimelyReminder.py**
   - This module provides a reminder system that alerts users when they've been playing for a certain amount of time. It generates reminders every 30 minutes, prompting users to take breaks. This helps promote healthy gaming habits and prevent excessive screen time.

### 5. **Voice_Threat_Detection.py**
   - This module uses machine learning or AI techniques to detect threatening voice inputs during gameplay or interactions. It helps ensure a safe and non-toxic environment for players.

### 6. **hate_speech.tsv**
   - A dataset containing examples of hate speech. This dataset is used for training models to detect hate speech in conversations, enabling the identification and filtering of inappropriate content in real-time used in **HarshwordsEncryption.py**.

### 7. **mainxlsx.xlsx**
   - A dataset that contains additional sentences and labels, likely used for detecting threats or offensive language within text, to be used in conjunction with the `Voice_Threat_Detection.py` module.

## How to Use

### 1. **Running the Flask API:**
   - To start the API, navigate to the directory containing the `DataEncryption.py` file.
   - Install the required dependencies:
     bash:
     pip install all_librarynames_imported_inthefile
     
   - Run the API:
     bash
     python FileName.py
     
   - The API will expose two endpoints: `/encrypt` and `/decrypt`, which you can use to send and receive encrypted/decrypted data.

