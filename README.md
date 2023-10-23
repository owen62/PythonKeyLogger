# PythonKeyLogger

**Disclaimer:** This project should be used for authorized testing or educational purposes only. You are free to copy, modify, and reuse the source code at your own risk.


## Description 

The PythonKeyLogger project aims to create a simple keylogger and expand its functionality with additional features:


- Operating System (OS) Information
- Collecting Mouse Clicks
- Audio Recording
- Collecting Clipboard Content
- Encrypting and Decrypting Logs Using a Randomly Generated Key
- Capturing Webcam Screens
- Capturing Screenshots

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

The script will run on your machine for 20 secs. Then the logs will be stored in a encrypted zipfile

### Decrypt the logs

To decrypt the zipfile, run the Decrypt.py script:

```bash
python Decrypt.py
```
You can now access to your logs.

## Notes

Please note that this repo is for educational purposes only. No contributors, major or minor, are responsible for any actions made by the software.

This project is not finished, it is ongoing and is being continuously enhanced with additional features (send the logs by email, Logging Setting, etc...)