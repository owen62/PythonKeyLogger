# PythonKeyLogger

**Disclaimer:** This project should be used for authorized testing or educational purposes only. You are free to copy, modify, and reuse the source code at your own risk.


## Description 

The PythonKeyLogger project aims to create a simple keylogger and expand its functionality with additional features:

- Mouse click logging
- Operating System (OS) information 
- Audio Recording
- Gathering clipboard content
- Encrypt and decrypt the logs using a key (Generated randomly)
- Capture Webcam screens
- Capture Screenshots

## Usage

### Installation
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
### Generate the key 
To encrypt the logs, generate a key using Fernet cryptography:

```bash
python GenerateKey.py
```

### Launch the keylogger

Once the key is generated, run the keylogger script:

```bash
python keylogger.py
```

The script will run on your machine indefinitely until you press the "esc" key.

### Decrypt the logs

To decrypt the logs, run the Decrypt.py script:

```bash
python Decrypt.py
```

## Notes

Please note that this repo is for educational purposes only. No contributors, major or minor, are responsible for any actions made by the software.

This project is not finished, it is ongoing and is being continuously enhanced with additional features (persistence, server integration for log storage, etc...)